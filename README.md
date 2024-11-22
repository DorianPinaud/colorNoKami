# Color No Kami

Color No Kami brings manga to life by adding vibrant colors to black-and-white pages! Powered by a U-Net model, it scrapes manga from [MangaDex API](https://api.mangadex.org/docs/), delivering an effortless and artistic experience for fans.

# 1. Database crafting

We create a database through an ETL process that transforms raw JSON data from the MangaDex API. This process pairs each chapter's full-color and monochrome versions, generates multiple stages of derived data, and structures it for easy use afterward.
