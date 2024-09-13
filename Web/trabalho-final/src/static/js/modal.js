
function successModal(title, text, timer = 3000) {
    Swal.fire({
        icon: 'success',
        title: title,
        html: text,
        showConfirmButton: false,
        timer: timer,
        customClass: {
            confirmButton: 'btn btn-primary waves-effect waves-light'
        },
        buttonsStyling: false
    });

}

function errorModal(title, text, timer = 3000) {
    Swal.fire({
        icon: 'error',
        title: title,
        html: text,
        timer: timer,
        showConfirmButton: false,
        customClass: {
            confirmButton: 'btn btn-danger waves-effect waves-light'
        },
        buttonsStyling: false
    });
}

function confirmModal(title, text, confirmButtonText, cancelButtonText, confirmFunction) {
    Swal.fire({
        title: title,
        html: text,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#34c38f',
        cancelButtonColor: '#f46a6a',
        confirmButtonText: confirmButtonText,
        cancelButtonText: cancelButtonText,
        customClass: {
            confirmButton: 'btn btn-primary waves-effect waves-light',
            cancelButton: 'btn btn-secondary waves-effect'
        },
        buttonsStyling: false
    }).then((result) => {
        if (result.isConfirmed) {
            confirmFunction();
        }
    });
}
