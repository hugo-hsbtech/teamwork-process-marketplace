# Decisões — registro de decisões entre fases (cross-phase)

Decisões que vinculam mais de uma seção ou mais de uma fase desta iniciativa.
Uma linha por decisão, com id estável `D###`. Decisões superadas são mantidas e
marcadas (`status: superseded`), nunca apagadas. Respostas rotineiras de seção
ficam no documento da fase e no `qa-log.md`, não aqui.

| id | decisão | escopo | tomada em (fase) | data | status | supersedes |
|----|---------|--------|------------------|------|--------|------------|
| D001 | Identidade do Host **sem login** no V1: o Host é reconhecido pelo vínculo do link, não por autenticação. O "como" técnico é do Technical Assessment. | origination → readiness | origination | 2026-06-03 | active | — |
| D002 | Sucessão do Host em desconexão (EC-02): política de produto definida pelo PO — o Host original reassume os direitos pelo mesmo link na reconexão. | readiness | readiness (Q023) | 2026-06-03 | active | — |
| D003 | RN-004 (revelação automática) posicionada como **V1.1**, não V1. Confirmação do Submitter original ainda pendente antes do freeze definitivo. | readiness → roadmap | readiness (Q018) | 2026-06-03 | active | — |
| D004 | Escopo **Excluído** declarado explicitamente pelo PO (sem persistência histórica de sessões no V1). | readiness | readiness (Q017) | 2026-06-03 | active | — |
| D005 | Alvo de latência de sincronização de estado: **~2 s p95**. Mecanismos de garantia são do Technical Assessment. | readiness → tech-assessment | readiness | 2026-06-03 | active | — |
| D006 | Nenhuma cifra de economia pode ser publicada até a correção da inconsistência aritmética (~10x); todas as cifras estão suprimidas. | origination → readiness → métricas | origination | 2026-06-03 | active | — |

<!-- END OF DOCUMENT -->
