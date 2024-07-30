import scrapy

class CapitaisPopulacaoSpider(scrapy.Spider):
    name = 'capitais_populacao'
    start_urls = ['https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_popula%C3%A7%C3%A3o']

    def parse(self, response):
        # Seleciona a tabela de capitais pelo corpo da tabela <tbody>
        tabela = response.xpath('//table[contains(@class, "wikitable")]/tbody')

        # Verifica se a tabela foi encontrada
        self.log(f'Tabela encontrada: {len(tabela)}')

        if len(tabela) == 0:
            self.log('Nenhuma tabela encontrada.')
            return

        # Itera sobre as linhas da tabela, começando da segunda linha de dados (pula o cabeçalho)
        for linha in tabela.xpath('.//tr')[1:]:  # [1:] para pular a linha do cabeçalho
            colunas = linha.xpath('.//td')
            self.log(f'Número de colunas na linha: {len(colunas)}')

            if len(colunas) >= 4:
                posicao = colunas[0].xpath('string()').get(default='').strip()
                capitais = colunas[1].xpath('.//a/text()').get(default='').strip()
                populacao_2022 = colunas[3].xpath('string()').get(default='').strip()

                # Adiciona logs para verificar os dados extraídos
                self.log(f'Posição: {posicao}, Capitais: {capitais}, População 2022: {populacao_2022}')

                # Cria um dicionário para armazenar os dados raspados
                yield {
                    'Posição': posicao,
                    'Capitais': capitais,
                    'População 2022': populacao_2022
                }
