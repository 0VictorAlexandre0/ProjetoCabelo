document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.querySelector("form");
    const campoData = document.getElementById("data");
    const campoHora = document.getElementById("hora");
    const mensagemData = document.getElementById("mensagem-data");
    const mensagemHora = document.getElementById("mensagem-hora");
    const campoServico = document.getElementById("servicos_id");
    const campoProfissional = document.getElementById("profissionais_id");

    if (!formulario || !campoData || !campoHora) return;

    if (campoServico && campoProfissional) {
        const profissionalAtual = campoProfissional.value;

        async function carregarProfissionais(preservarAtual = false) {
            const servicoId = campoServico.value;

            campoProfissional.innerHTML =
                '<option value="">Selecione um profissional</option>';
            campoProfissional.disabled = true;

            if (!servicoId) return;

            try {
                const resposta = await fetch(
                    `/agendamentos/profissionais/${servicoId}`
                );

                if (!resposta.ok) {
                    throw new Error("Erro ao buscar profissionais.");
                }

                const profissionais = await resposta.json();

                profissionais.forEach(function (profissional) {
                    const opcao = document.createElement("option");
                    opcao.value = profissional.id;
                    opcao.textContent = profissional.nome;

                    if (
                        preservarAtual &&
                        profissional.id == profissionalAtual
                    ) {
                        opcao.selected = true;
                    }

                    campoProfissional.appendChild(opcao);
                });

                campoProfissional.disabled = false;

            } catch (erro) {
                console.error(erro);
            }
        }

        campoServico.addEventListener("change", function () {
            carregarProfissionais(false);
        });

        if (campoServico.value) {
            carregarProfissionais(true);
        }
    }

    function validarAgendamento() {
        const agora = new Date();
        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);

        mensagemData.textContent = "";
        mensagemHora.textContent = "";

        if (!campoData.value) return true;

        const dataSelecionada = new Date(campoData.value + "T00:00:00");

        if (dataSelecionada < hoje) {
            mensagemData.textContent =
                "Não é permitido selecionar uma data passada.";
            return false;
        }

        if (
            dataSelecionada.getTime() === hoje.getTime() &&
            campoHora.value
        ) {
            const [hora, minuto] = campoHora.value.split(":").map(Number);
            const horarioSelecionado = new Date();

            horarioSelecionado.setHours(hora, minuto, 0, 0);

            if (horarioSelecionado <= agora) {
                mensagemHora.textContent =
                    "Não é permitido selecionar um horário que já passou.";
                return false;
            }
        }

        return true;
    }

    campoData.addEventListener("change", validarAgendamento);
    campoHora.addEventListener("change", validarAgendamento);

    formulario.addEventListener("submit", function (evento) {
        if (!validarAgendamento()) {
            evento.preventDefault();
        }
    });
});
