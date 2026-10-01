Source: https://github.com/dealcalcpro2026/dealcalc-core
Revision: 876db9c4fcc0ad7275d3fd58e72cda12cbe6d4e1
Extracted mao function unchanged. Reviewed pure math; no network or install hooks.
MIT; small young project, limited maintenance evidence. Vendored only this function to avoid unused numpy-financial/MCP dependencies.
We use rule_pct=100 and explicit buyer profit and costs, never a hidden 70% haircut.
