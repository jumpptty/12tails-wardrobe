0x1da4bf0 mov rax, rsp
0x1da4bf3 mov qword ptr [rax + 0x10], rbx
0x1da4bf7 mov qword ptr [rax + 0x18], rsi
0x1da4bfb push rdi
0x1da4bfc sub rsp, 0xe0
0x1da4c03 cmp byte ptr [rip + 0x1c59ebb], 0
0x1da4c0a mov esi, r9d
0x1da4c0d movaps xmmword ptr [rax - 0x18], xmm6
0x1da4c11 mov rdi, r8
0x1da4c14 movaps xmmword ptr [rax - 0x38], xmm8
0x1da4c19 mov rbx, rcx
0x1da4c1c movaps xmmword ptr [rax - 0x48], xmm9
0x1da4c21 movaps xmmword ptr [rax - 0x58], xmm10
0x1da4c26 mov qword ptr [rax + 8], rbp
0x1da4c2a mov rbp, rdx
0x1da4c2d jne 0x1da4c42
0x1da4c2f lea rcx, [rip + 0x1abd3ba]
0x1da4c36 call 0x23da00
0x1da4c3b mov byte ptr [rip + 0x1c59e83], 1
0x1da4c42 xor eax, eax
0x1da4c44 xorps xmm0, xmm0
0x1da4c47 cmp byte ptr [rip + 0x1c584ca], al
0x1da4c4d mov qword ptr [rbx], rax
0x1da4c50 movups xmmword ptr [rsp + 0x60], xmm0
0x1da4c55 mov dword ptr [rbx + 8], eax
0x1da4c58 movups xmmword ptr [rsp + 0x6c], xmm0
0x1da4c5d movups xmmword ptr [rsp + 0x50], xmm0
0x1da4c62 jne 0x1da4c77
0x1da4c64 lea rcx, [rip + 0x1a6d17d]
0x1da4c6b call 0x23da00
0x1da4c70 mov byte ptr [rip + 0x1c584a0], 1
0x1da4c77 cmp byte ptr [rip + 0x1c5849e], 0
0x1da4c7e movss xmm5, dword ptr [rdi]
0x1da4c82 movss xmm8, dword ptr [rdi + 4]
0x1da4c88 movaps xmm10, xmm5
0x1da4c8c movss xmm2, dword ptr [rdi + 8]
0x1da4c91 movaps xmm0, xmm8
0x1da4c95 mov rax, qword ptr [rip + 0x1a6d14c]
0x1da4c9c movaps xmm9, xmm2
0x1da4ca0 mov rcx, qword ptr [rax + 0xb8]
0x1da4ca7 movss xmm3, dword ptr [rcx + 0x18]
0x1da4cac movss xmm4, dword ptr [rcx + 0x1c]
0x1da4cb1 movss xmm1, dword ptr [rcx + 0x20]
0x1da4cb6 mulss xmm9, xmm4
0x1da4cbb mulss xmm0, xmm1
0x1da4cbf mulss xmm10, xmm1
0x1da4cc4 mulss xmm2, xmm3
0x1da4cc8 subss xmm9, xmm0
0x1da4ccd mulss xmm8, xmm3
0x1da4cd2 mulss xmm5, xmm4
0x1da4cd6 subss xmm10, xmm2
0x1da4cdb movss dword ptr [rsp + 0x30], xmm9
0x1da4ce2 subss xmm8, xmm5
0x1da4ce7 movss dword ptr [rsp + 0x34], xmm10
0x1da4cee movss dword ptr [rsp + 0x38], xmm8
0x1da4cf5 jne 0x1da4d0a
0x1da4cf7 lea rcx, [rip + 0x1a6d0ea]
0x1da4cfe call 0x23da00
0x1da4d03 mov byte ptr [rip + 0x1c58412], 1
0x1da4d0a xor edx, edx
0x1da4d0c lea rcx, [rsp + 0x30]
0x1da4d11 call 0x338290
0x1da4d16 comiss xmm0, dword ptr [rip + 0x125f85f]
0x1da4d1d jbe 0x1da4d30
0x1da4d1f divss xmm9, xmm0
0x1da4d24 divss xmm10, xmm0
0x1da4d29 divss xmm8, xmm0
0x1da4d2e jmp 0x1da4d4f
0x1da4d30 mov rax, qword ptr [rip + 0x1a6d0b1]
0x1da4d37 mov rcx, qword ptr [rax + 0xb8]
0x1da4d3e movss xmm9, dword ptr [rcx]
0x1da4d43 movss xmm10, dword ptr [rcx + 4]
0x1da4d49 movss xmm8, dword ptr [rcx + 8]
0x1da4d4f mov eax, dword ptr [rsp + 0x110]
0x1da4d56 cmp eax, 1
0x1da4d59 jg 0x1da4d65
0x1da4d5b movss xmm6, dword ptr [rip + 0x1194e2d]
0x1da4d63 jmp 0x1da4d79
0x1da4d65 dec eax
0x1da4d67 movd xmm6, esi
0x1da4d6b cvtdq2ps xmm6, xmm6
0x1da4d6e movd xmm0, eax
0x1da4d72 cvtdq2ps xmm0, xmm0
0x1da4d75 divss xmm6, xmm0
0x1da4d79 xorps xmm0, xmm0
0x1da4d7c comiss xmm0, xmm6
0x1da4d7f ja 0x1da4d93
0x1da4d81 movss xmm0, dword ptr [rip + 0x1194e0b]
0x1da4d89 comiss xmm6, xmm0
0x1da4d8c jbe 0x1da4d96
0x1da4d8e movaps xmm6, xmm0
0x1da4d91 jmp 0x1da4d96
0x1da4d93 xorps xmm6, xmm6
0x1da4d96 movaps xmmword ptr [rsp + 0x80], xmm11
0x1da4d9f mulss xmm6, dword ptr [rip + 0x125fbc9]
0x1da4da7 subss xmm6, dword ptr [rip + 0x125faa1]
0x1da4daf cmp esi, 5
0x1da4db2 jge 0x1da4dbf
0x1da4db4 movss xmm11, dword ptr [rip + 0x125fb23]
0x1da4dbd jmp 0x1da4dc8
0x1da4dbf movss xmm11, dword ptr [rip + 0x126023c]
0x1da4dc8 mov rsi, qword ptr [rbp + 0x60]
0x1da4dcc mov rbp, qword ptr [rsp + 0xf0]
0x1da4dd4 test rsi, rsi
0x1da4dd7 je 0x1da4fb8
0x1da4ddd mulss xmm6, dword ptr [rip + 0x1194da3]
0x1da4de5 movaps xmmword ptr [rsp + 0xc0], xmm7
0x1da4ded movaps xmm0, xmm6
0x1da4df0 call 0x308640
0x1da4df5 movaps xmm7, xmm0
0x1da4df8 movaps xmm0, xmm6
0x1da4dfb call 0x308bd0
0x1da4e00 xor r8d, r8d
0x1da4e03 lea rcx, [rsp + 0x40]
0x1da4e08 mov rdx, rsi
0x1da4e0b movaps xmm6, xmm0
0x1da4e0e call 0x2b36200
0x1da4e13 cmp byte ptr [rip + 0x1c582fd], 0
0x1da4e1a movaps xmm1, xmm7
0x1da4e1d mulss xmm1, dword ptr [rdi]
0x1da4e21 movaps xmm0, xmm7
0x1da4e24 mulss xmm0, dword ptr [rdi + 4]
0x1da4e29 mulss xmm7, dword ptr [rdi + 8]
0x1da4e2e mulss xmm9, xmm6
0x1da4e33 mulss xmm10, xmm6
0x1da4e38 mulss xmm8, xmm6
0x1da4e3d addss xmm9, xmm1
0x1da4e42 addss xmm10, xmm0
0x1da4e47 addss xmm8, xmm7
0x1da4e4c mulss xmm9, xmm11
0x1da4e51 mulss xmm10, xmm11
0x1da4e56 addss xmm9, dword ptr [rax]
0x1da4e5b mulss xmm8, xmm11
0x1da4e60 addss xmm10, dword ptr [rax + 4]
0x1da4e66 addss xmm8, dword ptr [rax + 8]
0x1da4e6c movss dword ptr [rbx], xmm9
0x1da4e71 movss dword ptr [rbx + 4], xmm10
0x1da4e77 movss dword ptr [rbx + 8], xmm8
0x1da4e7d jne 0x1da4e92
0x1da4e7f lea rcx, [rip + 0x1a6cf62]
0x1da4e86 call 0x23da00
0x1da4e8b mov byte ptr [rip + 0x1c58285], 1
0x1da4e92 cmp byte ptr [rip + 0x1c58779], 0
0x1da4e99 mov rdx, qword ptr [rip + 0x1a6cf48]
0x1da4ea0 mov rax, qword ptr [rdx + 0xb8]
0x1da4ea7 movss xmm6, dword ptr [rax + 0x18]
0x1da4eac movss xmm7, dword ptr [rax + 0x1c]
0x1da4eb1 addss xmm6, xmm6
0x1da4eb5 movss xmm11, dword ptr [rax + 0x20]
0x1da4ebb addss xmm7, xmm7
0x1da4ebf addss xmm11, xmm11
0x1da4ec4 addss xmm6, xmm9
0x1da4ec9 addss xmm7, xmm10
0x1da4ece addss xmm11, xmm8
0x1da4ed3 jne 0x1da4eef
0x1da4ed5 lea rcx, [rip + 0x1a6cf0c]
0x1da4edc call 0x23da00
0x1da4ee1 mov rdx, qword ptr [rip + 0x1a6cf00]
0x1da4ee8 mov byte ptr [rip + 0x1c58723], 1
0x1da4eef mov rax, qword ptr [rdx + 0xb8]
0x1da4ef6 mov rcx, qword ptr [rip + 0x1abd0f3]
0x1da4efd movsd xmm8, qword ptr [rax + 0x24]
0x1da4f03 cmp dword ptr [rcx + 0xe4], 0
0x1da4f0a mov edi, dword ptr [rax + 0x2c]
0x1da4f0d jne 0x1da4f14
0x1da4f0f call 0x23dce0
0x1da4f14 movss xmm3, dword ptr [rip + 0x1194c80]
0x1da4f1c lea r8, [rsp + 0x50]
0x1da4f21 mov qword ptr [rsp + 0x28], 0
0x1da4f2a lea rdx, [rsp + 0x40]
0x1da4f2f lea rcx, [rsp + 0x30]
0x1da4f34 mov dword ptr [rsp + 0x20], 1
