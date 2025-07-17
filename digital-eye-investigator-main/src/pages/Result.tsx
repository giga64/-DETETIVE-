import { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";
import { UserSearch, ArrowLeft } from "lucide-react";

interface SearchHistory {
  id: string;
  timestamp: string;
  document: string;
  result: string;
}

const Result = () => {
  const location = useLocation();
  const document = location.state?.document || "";
  const [result, setResult] = useState("");
  const [history, setHistory] = useState<SearchHistory[]>([]);

  // Simular resposta da API
  useEffect(() => {
    if (document) {
      const simulatedResult = `
RELATÓRIO DE INVESTIGAÇÃO DIGITAL
================================

Documento investigado: ${document}
Data da consulta: ${new Date().toLocaleString('pt-BR')}
Status: CONSULTA REALIZADA

Informações básicas:
- Tipo: ${document.length === 11 ? 'CPF' : 'CNPJ'}
- Número: ${document}
- Situação: ATIVA

Observações:
Esta é uma demonstração da ferramenta.
Os dados apresentados são fictícios.

Fim do relatório.
================================`;

      setResult(simulatedResult);

      // Adicionar ao histórico
      const newSearch: SearchHistory = {
        id: Date.now().toString(),
        timestamp: new Date().toLocaleString('pt-BR'),
        document,
        result: simulatedResult
      };

      // Recuperar histórico existente
      const existingHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
      const updatedHistory = [newSearch, ...existingHistory].slice(0, 5); // Manter apenas os 5 mais recentes
      
      setHistory(updatedHistory);
      localStorage.setItem('searchHistory', JSON.stringify(updatedHistory));
    }
  }, [document]);

  // Carregar histórico na inicialização
  useEffect(() => {
    const savedHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    setHistory(savedHistory);
  }, []);

  if (!document) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">Nenhuma busca encontrada</p>
          <Link to="/" className="text-primary hover:underline">
            Voltar para a busca
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="w-full max-w-sm mx-auto">
        <div className="bg-card border border-border rounded-lg shadow-lg p-6">
          {/* Cabeçalho */}
          <div className="text-center mb-6">
            <div className="flex items-center justify-center gap-2 mb-2">
              <UserSearch className="h-6 w-6 text-primary" />
              <h1 className="text-xl font-semibold text-foreground">
                Relatório da busca
              </h1>
            </div>
          </div>

          {/* Relatório */}
          <div className="mb-8">
            <div className="bg-secondary border-2 border-dashed border-border rounded p-4">
              <pre className="text-xs font-mono text-secondary-foreground whitespace-pre-wrap overflow-x-auto">
                {result}
              </pre>
            </div>
          </div>

          {/* Histórico */}
          {history.length > 0 && (
            <div className="mb-6">
              <h2 className="text-lg font-medium text-foreground mb-3 flex items-center gap-2">
                <UserSearch className="h-4 w-4" />
                Suas últimas buscas
              </h2>
              <div className="space-y-2">
                {history.map((item) => (
                  <details key={item.id} className="border border-border rounded">
                    <summary className="cursor-pointer p-3 hover:bg-muted text-sm">
                      {item.timestamp} - {item.document}
                    </summary>
                    <div className="px-3 pb-3">
                      <div className="bg-secondary border border-border rounded p-2 mt-2">
                        <pre className="text-xs font-mono text-secondary-foreground whitespace-pre-wrap overflow-x-auto">
                          {item.result}
                        </pre>
                      </div>
                    </div>
                  </details>
                ))}
              </div>
            </div>
          )}

          {/* Link para nova busca */}
          <div className="text-center">
            <Link 
              to="/" 
              className="inline-flex items-center gap-2 text-primary hover:underline"
            >
              <ArrowLeft className="h-4 w-4" />
              Nova busca
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Result;