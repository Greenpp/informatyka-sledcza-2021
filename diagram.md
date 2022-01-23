# Diagram poglądowy systemu

```mermaid
stateDiagram
    Nadawca --> Proxy
    state Proxy {
        Filtr_Słownikowy --> Filtr_RBL
        Filtr_RBL --> Filtr_VirusTotal
    }
    Proxy --> BazaDanych
    Proxy --> Kwarantanna
    Proxy --> Odbiorca
```
