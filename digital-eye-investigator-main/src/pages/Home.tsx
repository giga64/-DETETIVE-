import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const Home = () => {
  const [document, setDocument] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const validateDocument = (value: string) => {
    const cleaned = value.replace(/\D/g, "");
    if (cleaned.length === 11 || cleaned.length === 14) {
      return true;
    }
    return false;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!document.trim()) {
      setError("Por favor, insira um CPF ou CNPJ");
      return;
    }

    if (!validateDocument(document)) {
      setError("CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos");
      return;
    }

    // Simular busca e redirecionar para resultado
    navigate("/resultado", { state: { document: document.replace(/\D/g, "") } });
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-sm mx-auto">
        <div className="bg-card border border-border rounded-lg shadow-lg p-8">
          {/* Cabeçalho */}
          <div className="text-center mb-6">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Search className="h-6 w-6 text-primary" />
              <h1 className="text-xl font-semibold text-foreground">
                Detective CPF/CNPJ
              </h1>
            </div>
            <p className="text-sm text-muted-foreground">
              Insira o CPF ou CNPJ para a busca.
            </p>
          </div>

          {/* Formulário */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input
                type="text"
                placeholder="Ex: 01234567890"
                value={document}
                onChange={(e) => setDocument(e.target.value)}
                className="text-center"
                maxLength={18}
              />
              {error && (
                <p className="text-sm text-destructive mt-2 text-center">
                  {error}
                </p>
              )}
            </div>

            <Button 
              type="submit" 
              className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
            >
              Iniciar investigação
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Home;