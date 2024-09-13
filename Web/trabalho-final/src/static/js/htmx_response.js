// document.addEventListener('htmx:afterRequest', function (event) {
//     if (event.detail.target.id === "form-send-message") {
//         if (event.detail.xhr.status === 201) {
//             successModal('Depoimento enviado', 'Seu depoimento foi enviada com sucesso!');
//         } else if (event.detail.xhr.status == 400) {
//             const response = JSON.parse(event.detail.xhr.response);
//             errorModal('Erro ao enviar depoimento', response.message);
//         }
//         else if (event.detail.xhr.status == 422) {
//             let response = JSON.parse(event.detail.xhr.response);
//             let fields = '<div class="text-center">';
//             response.detail.forEach(element => {
//                 fields += `<strong>${element.loc[1]}</strong><br>`;
//             });
//             fields += '</div>';
//             errorModal('Erro ao enviar depoimento', 'Os seguintes campos são obrigatórios:<br>' + fields);
//         }
//         else if (event.detail.xhr.status == 500) {
//             errorModal('Erro ao enviar mensagem', 'Ocorreu um erro interno no servidor, tente novamente mais tarde.');
//         }
//     }
// });
