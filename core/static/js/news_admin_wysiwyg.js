document.addEventListener("DOMContentLoaded", function () {
    if (typeof tinymce === "undefined") return;
    const selector = "textarea.news-wysiwyg";
    if (!document.querySelector(selector)) return;

    tinymce.init({
        selector,
        height: 520,
        menubar: false,
        branding: false,
        plugins: "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table wordcount",
        toolbar:
            "undo redo | blocks | bold italic underline | forecolor backcolor | " +
            "alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | " +
            "link image media | removeformat code preview",
        content_style:
            "body { font-family: Inter, Arial, sans-serif; font-size: 15px; line-height: 1.65; }",
    });
});
