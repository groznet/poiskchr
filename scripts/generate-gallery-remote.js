const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');

const BASE_REMOTE_URL = 'https://files.groznet.com/poiskchr/news/';
const CONTENT_DIR = path.join(__dirname, '../content/news');

const isImage = (url) => /\.(jpg|jpeg|png|webp|gif)$/i.test(url);

async function processPost(postDir) {
    // Determine the relative path (e.g., "2025/08/any-post-slug")
    const relativePath = path.relative(CONTENT_DIR, postDir).replace(/\\/g, '/');
    
    // The gallery images are in the /images/ subfolder of the post
    const remoteImagesUrl = `${BASE_REMOTE_URL}${relativePath}/images/`;

    try {
        const response = await axios.get(remoteImagesUrl);
        const $ = cheerio.load(response.data);
        
        let images = [];

        $('a').each((i, el) => {
            const href = $(el).attr('href');
            // Ignore parent directory links and non-images
            if (href && !href.startsWith('?') && !href.startsWith('/') && isImage(href)) {
                // Ensure we get just the filename
                const cleanName = href.split('/').pop();
                images.push(cleanName);
            }
        });

        if (images.length > 0) {
            // Sorting: If filenames are random strings, alpha sort is safest. 
            // If they are numbers, this handles that too.
            images.sort((a, b) => a.localeCompare(b, undefined, {numeric: true, sensitivity: 'base'}));

            const output = {
                remote_base_url: remoteImagesUrl,
                featured_image: `${BASE_REMOTE_URL}${relativePath}/feature.jpg`,
                images: images
            };

            fs.writeFileSync(
                path.join(postDir, 'gallery.json'),
                JSON.stringify(output, null, 4)
            );
            console.log(`✅ Generated: ${relativePath}/gallery.json`);
        }
    } catch (error) {
        // If the folder doesn't exist remotely, it just skips quietly
        // console.error(`❌ Missing remote: ${relativePath}`);
    }
}

function walk(dir) {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            // Check if this folder is a Post (contains index.md or .md file)
            const isPostFolder = fs.readdirSync(fullPath).some(f => f.endsWith('.md'));

            if (isPostFolder) {
                processPost(fullPath);
            } else {
                // It's a year or month folder, keep digging
                walk(fullPath);
            }
        }
    });
}

console.log("🚀 Starting remote gallery scan...");
walk(CONTENT_DIR);