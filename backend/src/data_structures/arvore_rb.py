# ============================================================
# ARQUIVO: arvore_rb.py
# O QUE FAZ: implementa a Árvore Rubro-Negra.
# É um "caderno esperto" que organiza produtos por SKU
# para busca rápida O(log n).
#
# ANALOGIA: uma árvore genealógica onde cada pessoa tem no
# máximo 2 filhos (esquerda = menor, direita = maior).
# As cores (vermelho/preto) mantêm a árvore equilibrada.
# ============================================================

VERMELHO = "VERMELHO"
PRETO = "PRETO"


class No:
    """Um 'nó' é uma caixinha que guarda um produto."""

    def __init__(self, chave, valor=None):
        self.chave = chave          # SKU (usado para ordenar)
        self.valor = valor or {}    # dados do produto
        self.cor = VERMELHO         # todo nó novo nasce vermelho
        self.esq = None             # filho esquerdo (menores)
        self.dir = None             # filho direito (maiores)
        self.pai = None             # ponteiro para o pai


class ArvoreRB:
    """A árvore inteira."""

    def __init__(self):
        # 'nil' é um nó sentinela que representa "vazio".
        # Truque: usamos sempre self.nil em vez de None,
        # para evitar erros de NoneType.
        self.nil = No(None)
        self.nil.cor = PRETO
        self.nil.esq = self.nil
        self.nil.dir = self.nil
        self.raiz = self.nil
        self._tamanho = 0

    # ---------- ROTAÇÕES ----------
    def _rot_esq(self, x):
        """Rotação à esquerda em torno de x."""
        y = x.dir
        x.dir = y.esq
        if y.esq is not self.nil:
            y.esq.pai = x
        y.pai = x.pai
        if x.pai is self.nil:
            self.raiz = y
        elif x is x.pai.esq:
            x.pai.esq = y
        else:
            x.pai.dir = y
        y.esq = x
        x.pai = y

    def _rot_dir(self, x):
        """Rotação à direita (espelho da anterior)."""
        y = x.esq
        x.esq = y.dir
        if y.dir is not self.nil:
            y.dir.pai = x
        y.pai = x.pai
        if x.pai is self.nil:
            self.raiz = y
        elif x is x.pai.dir:
            x.pai.dir = y
        else:
            x.pai.esq = y
        y.dir = x
        x.pai = y

    # ---------- INSERÇÃO ----------
    def inserir(self, chave, valor=None):
        z = No(chave, valor)
        z.esq = z.dir = self.nil
        y = self.nil
        x = self.raiz
        # Desce até achar o lugar certo
        while x is not self.nil:
            y = x
            if z.chave < x.chave:
                x = x.esq
            elif z.chave > x.chave:
                x = x.dir
            else:
                x.valor = valor   # já existe → atualiza
                return x
        z.pai = y
        if y is self.nil:
            self.raiz = z
        elif z.chave < y.chave:
            y.esq = z
        else:
            y.dir = z
        z.cor = VERMELHO
        self._corrige_insercao(z)
        self._tamanho += 1
        return z

    def _corrige_insercao(self, z):
        """Sobe a árvore corrigindo violações de cor."""
        while z.pai.cor == VERMELHO:
            if z.pai is z.pai.pai.esq:
                y = z.pai.pai.dir   # tio
                if y.cor == VERMELHO:
                    z.pai.cor = PRETO
                    y.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z is z.pai.dir:
                        z = z.pai
                        self._rot_esq(z)
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self._rot_dir(z.pai.pai)
            else:
                y = z.pai.pai.esq
                if y.cor == VERMELHO:
                    z.pai.cor = PRETO
                    y.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z is z.pai.esq:
                        z = z.pai
                        self._rot_dir(z)
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self._rot_esq(z.pai.pai)
            if z is self.raiz:
                break
        self.raiz.cor = PRETO

    # ---------- BUSCA ----------
    def buscar(self, chave):
        x = self.raiz
        while x is not self.nil and chave != x.chave:
            if chave < x.chave:
                x = x.esq
            else:
                x = x.dir
        return x if x is not self.nil else None

    # ---------- REMOÇÃO ----------
    def _transplante(self, u, v):
        if u.pai is self.nil:
            self.raiz = v
        elif u is u.pai.esq:
            u.pai.esq = v
        else:
            u.pai.dir = v
        v.pai = u.pai

    def _minimo(self, x):
        while x.esq is not self.nil:
            x = x.esq
        return x

    def remover(self, chave):
        z = self.buscar(chave)
        if z is None:
            return False
        y = z
        cor_original = y.cor
        if z.esq is self.nil:
            x = z.dir
            self._transplante(z, z.dir)
        elif z.dir is self.nil:
            x = z.esq
            self._transplante(z, z.esq)
        else:
            y = self._minimo(z.dir)
            cor_original = y.cor
            x = y.dir
            if y.pai is z:
                x.pai = y
            else:
                self._transplante(y, y.dir)
                y.dir = z.dir
                y.dir.pai = y
            self._transplante(z, y)
            y.esq = z.esq
            y.esq.pai = y
            y.cor = z.cor
        if cor_original == PRETO:
            self._corrige_remocao(x)
        self._tamanho -= 1
        return True

    def _corrige_remocao(self, x):
        while x is not self.raiz and x.cor == PRETO:
            if x is x.pai.esq:
                w = x.pai.dir
                if w.cor == VERMELHO:
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rot_esq(x.pai)
                    w = x.pai.dir
                if w.esq.cor == PRETO and w.dir.cor == PRETO:
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.dir.cor == PRETO:
                        w.esq.cor = PRETO
                        w.cor = VERMELHO
                        self._rot_dir(w)
                        w = x.pai.dir
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.dir.cor = PRETO
                    self._rot_esq(x.pai)
                    x = self.raiz
            else:
                w = x.pai.esq
                if w.cor == VERMELHO:
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rot_dir(x.pai)
                    w = x.pai.esq
                if w.dir.cor == PRETO and w.esq.cor == PRETO:
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.esq.cor == PRETO:
                        w.dir.cor = PRETO
                        w.cor = VERMELHO
                        self._rot_esq(w)
                        w = x.pai.esq
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.esq.cor = PRETO
                    self._rot_dir(x.pai)
                    x = self.raiz
        x.cor = PRETO

    # ---------- VALIDAÇÃO (usada nos testes) ----------
    def validar(self):
        """Confere se as 3 regras rubro-negras estão OK."""
        if self.raiz.cor != PRETO:
            return False, "Raiz não é preta"

        def _bh(no):
            if no is self.nil:
                return 1
            if no.cor == VERMELHO:
                if no.esq.cor == VERMELHO or no.dir.cor == VERMELHO:
                    return -1
            e = _bh(no.esq)
            d = _bh(no.dir)
            if e == -1 or d == -1 or e != d:
                return -1
            return e + (1 if no.cor == PRETO else 0)

        if _bh(self.raiz) == -1:
            return False, "Violação de propriedade RB"
        return True, "OK"

    def __len__(self):
        return self._tamanho