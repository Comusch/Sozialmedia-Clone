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