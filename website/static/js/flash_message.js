document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#deleteNotificationButton').addEventListener('click', function () {
        let element = document.querySelector('#notification');
        element.remove();
    });
});
