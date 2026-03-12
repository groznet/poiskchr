const fs = require('fs');
const path = require('path');

const CONTENT_DIR = path.join(__dirname, '../content/news');

function walk(dir) {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            walk(fullPath);
        }

        if (file === 'images') {
            const imagesDir = fullPath;
            const postDir = path.dirname(imagesDir);

            const images = fs.readdirSync(imagesDir)
                .filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f))
                .sort((a, b) => {
                    return parseInt(a) - parseInt(b);
                });

            const output = {
                images: images
            };

            fs.writeFileSync(
                path.join(postDir, 'gallery.json'),
                JSON.stringify(output, null, 4)
            );

            console.log(`Generated gallery.json in ${postDir}`);
        }
    });
}

walk(CONTENT_DIR);
