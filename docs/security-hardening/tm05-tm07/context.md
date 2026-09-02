# Hardening analysis context

This derived analysis was prepared from the RAG repository at `77e6174` and the
Kujo repository at `2a5612c`. The source roots used during review were the local
RAG and Kujo checkouts.

| Evidence | Reader-facing title | Path | SHA-256 |
| --- | --- | --- | --- |
| E-TM | RAG threat-model packet | `docs/security-reviews/TM-2026-08-RAG-draft.md` | `5dd42a2b43c9a367078fcbb68f37a15da04da784f719b4deb8dfd5c09e18bf8c` |
| E-QSRC | Qdrant synchronization implementation | `src/vector_backend.kujo` | `4401d45681bb74d20ff0a8a0f4d5989111328e58b3f62e741be18d1c443b0b95` |
| E-QDOC | Qdrant backend contract | `docs/qdrant-vector-backend.md` | `137c6f8d4af6a6856db32fd073c9c95a677ad2fff1f753bfecf0697fd4b35b54` |
| E-QTEST | Qdrant security regression | `tests/test_qdrant_security.kujo` | `3f8955794aaa3a8c1e40726600288b4fdf2494c7a5fe7ea4ca6a1029c9dcbb27` |
| E-KUJO-FS | Kujo filesystem boundary sources | Kujo `src/path_security.rs`, `src/interpreter/native_functions/filesystem.rs`, and `docs/STANDARD_LIBRARY_REFERENCE.md` | `241d60062740f476c05fb93d155e3151711d75e9940b22f5632e6c942b2dbed0` |

The seven source files represented above have collection digest
`1ac17b7674f2a42a0da9ae654838ec8503543eaf8f9630f7e1348c1ba3ad0032`.
The Kujo filesystem subset digest is recorded separately because it belongs to
a different repository and revision.
