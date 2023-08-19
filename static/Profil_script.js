document.addEventListener('DOMContentLoaded', () => {
    const loadCommentButtons = document.querySelectorAll('.load-comments-button');

    loadCommentButtons.forEach(button => {
        button.addEventListener('click', () => {
            const postID = button.getAttribute('data-post-id');
            const commentSection = document.querySelector(`#comment-section-${postID}`);
            commentSection.style.display = commentSection.style.display === 'none' ? 'block' : 'none';
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const BotsloaderButton = document.querySelector('.show_bots_button');

        BotsloaderButton.addEventListener('click', () => {
            const commentSection = document.querySelector(`.bots-container`);
            commentSection.style.display = commentSection.style.display === 'none' ? 'block' : 'none';
        });
});