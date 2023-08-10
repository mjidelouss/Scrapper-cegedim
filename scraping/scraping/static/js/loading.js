document.addEventListener('DOMContentLoaded', function () {
    const importButton = document.getElementById('import-button');
    const image = document.getElementById('womenThink');
    const loader = document.getElementById('loader');

    importButton.addEventListener('click', function () {
        // Hide the image and show the loader
        image.style.display = 'none';
        loader.style.display = 'grid';

        // Simulate a delay (replace with actual backend processing)
        setTimeout(function () {
            // Hide the loader and show the image
            loader.style.display = 'none';
            image.style.display = 'block';
        }, 5 * 3600000); // Adjust the delay as needed
    });
});
