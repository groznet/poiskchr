Process only the newly added Hugo posts in:

`news/2026/09/`

Do NOT process posts from previous years or months.

Inside `news/2026/09/`, find all `index.md` files that do NOT already contain Hugo front matter.

A valid processed file starts with:

+++
date = 'YYYY-MM-DDTHH:MM:SS+03:00'
draft = false
title = 'Post title'
slug = 'post-slug'
+++

Only process files that are missing this front matter. Leave any file that already has front matter completely unchanged.

For each unprocessed `index.md`:

1. Read the raw content copied from the client's original page.

2. The content usually contains the post text followed by a relative publication time such as:

   * `3 days ago`
   * `2 days ago`
   * `5 hours ago`
   * `yesterday`
   * `today`
   * or similar wording.

3. Determine the original publication date from that relative timestamp, using the current date/time as the reference point.

4. Use the `+03:00` timezone for the Hugo `date` value.

5. Determine the post title from the copied content. If there is no clearly identifiable title, create a concise title based on the post content.

6. Generate a URL-safe ASCII slug:

   * lowercase
   * hyphens instead of spaces
   * no Cyrillic characters
   * no special characters
   * reasonably short
   * descriptive of the post

7. Set:

`draft = false`

8. Add the following front matter to the beginning of the file:

+++
date = 'YYYY-MM-DDTHH:MM:SS+03:00'
draft = false
title = 'Post title'
slug = 'post-slug'
+++

9. Preserve the original post text exactly as much as possible. Do not rewrite, summarize, translate, or stylistically edit the client's content.

10. Remove the relative publication-time text (for example, `3 days ago`) from the post body because that information is now represented by the Hugo `date` field.

11. Do not add any other front-matter fields.

12. Do not modify, rename, move, or delete any other files.

13. Do not process any `index.md` that already contains front matter.

14. If the publication date cannot be determined reliably from the available information, do not guess. Leave that file unchanged and report it to me.

After processing, give me a concise summary containing:

* number of files processed
* filenames processed
* date/title/slug generated for each
* any files skipped because they already had front matter
* any files skipped because their publication date could not be determined

Before making changes, inspect the directory and identify exactly which files qualify for processing.