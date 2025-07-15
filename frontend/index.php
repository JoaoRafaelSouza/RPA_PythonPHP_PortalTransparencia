<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <!-- Tailwind CDN (manter apenas para dev, substitua em produção) -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Define ícone da aba -->
    <link rel="icon" href="data:," />

    <title>Consulta de Beneficiários</title>

    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
    </style>
</head>

<body class="bg-gray-100 text-gray-900 min-h-screen flex items-center justify-center p-4">

    <main class="w-full max-w-2xl bg-white shadow-xl rounded-xl p-6">
        <h1 class="text-2xl font-bold mb-4">Buscar Beneficiário de Programa Social</h1>

        <form id="formBusca" class="space-y-4 max-w-md mx-auto">
            <label for="busca" class="block font-semibold">Nome, CPF ou NIS:</label>
            <input type="text" name="busca" id="busca" class="w-full p-2 border rounded" required />

            <label for="filtro" class="block font-semibold">Filtro obrigatório:</label>
            <select id="filtro" disabled class="w-full p-2 border rounded bg-gray-200">
                <option selected>BENEFICIÁRIO DE PROGRAMA SOCIAL</option>
            </select>

            <button type="submit"
                class="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition">Buscar</button>
        </form>

        <div class="mt-6">
            <h2 class="text-xl font-semibold mt-8 max-w-md mx-auto">Resultado:</h2>
            <pre id="resultado" class="max-w-md mx-auto bg-white p-4 rounded shadow mt-2 overflow-auto"></pre>
        </div>
    </main>

    <script>
        document.getElementById("formBusca").addEventListener("submit", function (e) {
            e.preventDefault();

            const busca = document.getElementById("busca").value.trim();
            const resultado = document.getElementById("resultado");

            if (busca === "") {
                alert("Informe um nome, CPF ou NIS");
                return;
            }

            let payload = {};
            if (/^\d{11}$/.test(busca)) {
                payload.cpf = busca;
            } else if (/^\d{10,}$/.test(busca)) {
                payload.nis = busca;
            } else {
                payload.nome = busca;
            }

            fetch("http://localhost:8000/api/buscar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            })
                .then(res => {
                    if (!res.ok) throw new Error("Erro na API");
                    return res.json();
                })
                .then(data => {
                    resultado.textContent = JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    resultado.textContent = "Erro: " + error.message;
                });
        });
    </script>
</body>

</html>