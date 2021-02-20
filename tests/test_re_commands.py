"""Test regular expression parsing commands"""


def test_e(mapdl, cleared):
    mapdl.et("", 183)
    n0 = mapdl.n("", 0, 0, 0)
    n1 = mapdl.n("", 1, 0, 0)
    n2 = mapdl.n("", 1, 1, 0)
    n3 = mapdl.n("", 0, 1, 1)
    n4 = mapdl.n("", 0, 1, -1)
    e0 = mapdl.e(n0, n1, n2, n3)
    assert e0 == 1
    e1 = mapdl.e(n0, n1, n2, n4)
    assert e1 == 2


def test_et(mapdl, cleared):
    n_plane183 = mapdl.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl.get_value("ETYP", item1="NUM", it1num="MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl.et(17, "PLANE183")
    assert n_plane183 == 17


def test_kbetw(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    assert mapdl.kbetw(k0, k1) == 3


def test_kdist(cleared, mapdl):
    kp0 = (0, 10, -3)
    kp1 = (-1E10, 10, 4)

    knum0 = mapdl.k("", *kp0)
    knum1 = mapdl.k("", *kp1)
    xdist, ydist, zdist = mapdl.kdist(knum0, knum1)
    assert xdist == kp1[0] - kp0[0]
    assert ydist == kp1[1] - kp0[1]
    assert zdist == kp1[2] - kp0[2]


# kept here for potential usage
# def test_kfill(cleared, mapdl):
#     mapdl.clear()
#     mapdl.prep7()
#     kp0 = (0, 0, 0)
#     kp1 = (10, 0, 0)

#     knum0 = mapdl.k("", *kp0)
#     knum1 = mapdl.k("", *kp1)
#     mapdl.kfill(knum0, knum1, 8, ninc=1)


def test_kl(cleared, mapdl):
    kp0 = (0, 0, 0)
    kp1 = (10, 0, 0)
    knum0 = mapdl.k("", *kp0)
    knum1 = mapdl.k("", *kp1)
    lnum = mapdl.l(knum0, knum1)

    assert mapdl.kl(lnum, 0.5) == knum1 + 1


def test_knode(cleared, mapdl):
    nnum = mapdl.n('', 1, 2, 3)
    knum1 = mapdl.knode('', nnum)
    assert knum1 == 1


def test_l2ang(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)
    k2 = mapdl.k("", 0, 0, 0.5)
    carc0 = mapdl.circle(k0, 1, k1)
    carc1 = mapdl.circle(k2, 1, k1)
    lnum = mapdl.l2ang(carc0[0], carc1[0], 90, 90)
    assert lnum == 11


def test_l2tan(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)

    k2 = mapdl.k("", -1.5, 1.5, 0)
    k3 = mapdl.k("", -1.5, 1.5, 1)

    carc0 = mapdl.circle(k0, 1, k1, arc=90)
    carc1 = mapdl.circle(k2, 1, k3, arc=90)
    lnum = mapdl.l2tan(1, 2)
    assert lnum == 3

def test_kcenter(cleared, mapdl):
    # compute the center of a circle
    x, y, z = 0+1j, 1+0j, 0-1j

    # commented out should we wish to confirm the coordinates
    # w = z-x
    # w /= y-x
    # c = (x-y)*(w-abs(w)**2)/2j/w.imag-x

    k0 = mapdl.k("", x.real, x.imag, 0)
    k1 = mapdl.k("", y.real, y.imag, 0)
    k2 = mapdl.k("", z.real, z.imag, 0)
    k3 = mapdl.kcenter('KP', k0, k1, k2)
    assert k3 == k2 + 1


def test_blc4(cleared, mapdl):
    assert mapdl.blc4(0, 0, 1, 1) == 1


def test_kbetw(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    assert mapdl.kbetw(k0, k1) == 3


def test_asba(cleared, mapdl):
    anum0 = mapdl.blc4(0, 0, 1, 1)
    anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
    aout = mapdl.asba(anum0, anum1)
    assert aout == 3


def test_cyl4(cleared, mapdl):
    assert mapdl.cyl4(0, 0, 1, depth=10) == 1


def test_k(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    assert k0 == 1
    k1 = mapdl.k(2, 0, 0, 1)
    assert k1 == 2


def test_l(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    assert l0 == 1


def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2)
    assert a0 == 1


def test_v(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    k3 = mapdl.k("", 0, 0, 1)
    v0 = mapdl.v(k0, k1, k2, k3)
    assert v0 == 1


def test_n(cleared, mapdl):
    n0 = mapdl.n("", 0, 0, 0)
    assert n0 == 1
    n1 = mapdl.n(2, 0, 0, 1)
    assert n1 == 2


def test_bsplin(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 2, 1, 0)
    l0 = mapdl.bsplin(k0, k1, k2)
    assert l0 == 1


def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert a0 == 1


def test_al(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    a0 = mapdl.al(l0, l1, l2, l3)
    assert a0 == 1
