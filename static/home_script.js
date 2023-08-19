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

function deletePost(postId){
    fetch('/delete-post', {
        method: 'POST',
        body: JSON.stringify({ postId: postId }),
    }).then((_res) => {
        window.location.href = "/";
    })
}

function deleteComment(commentId){
    fetch('/delete-comment', {
        method: 'POST',
        body: JSON.stringify({ commentId: commentId }),
    }).then((_res) => {
        window.location.href = "/";
    })
}