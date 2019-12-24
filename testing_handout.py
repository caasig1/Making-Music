import make_some_noise as noise
import numpy as np

def test_simple_wave_equal():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(100, 1, 1)
    assert s1 == s2

def test_simple_wave_not_equal():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(101, 1, 1)
    s3 = noise.SimpleWave(100, 0.5, 1)
    s4 = noise.SimpleWave(100, 1, 0.5)
    assert s1 != s2 and s1 != s3 and s1 != s4

def test_simple_wave_add():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(150, 1, 1)
    s3 = s1 + s2
    waves = s3.get_waves()
    assert len(waves) == 2
    assert any(s1 == s for s in waves)
    assert any(s2 == s for s in waves)

def test_simple_wave_get_duration():
    s1 = noise.SimpleWave(100, 0.9, 0.5)
    assert abs(s1.get_duration() - 0.9) < 0.0001

def test_simple_wave_play():
    s1 = noise.SimpleWave(100, 1, 0.8)
    assert s1.play().max() <= 1
    assert s1.play().min() >= -1

def test_complex_wave_add():
    c1 = noise.ComplexWave([])
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(150, 1, 1)
    c2 = noise.ComplexWave([s2])
    c3 = c1 + s1 + c2
    waves = c3.get_waves()
    assert len(waves) == 2
    assert any(s1 == s for s in waves)
    assert any(s2 == s for s in waves)

def test_complex_wave_complexity():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(101, 1, 1)
    s3 = noise.SimpleWave(100, 0.5, 1)
    s4 = noise.SimpleWave(100, 1, 0.5)
    c1 = noise.ComplexWave([s1, s2, s3, s4])
    assert c1.complexity() == 4

def test_complex_wave_get_waves():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(101, 1, 1)
    s3 = noise.SimpleWave(100, 0.5, 1)
    s4 = noise.SimpleWave(100, 1, 0.5)
    simple_waves = [s1, s2, s3, s4]
    c1 = noise.ComplexWave(simple_waves)
    waves = c1.get_waves()
    assert len(waves) == 4
    for wave in simple_waves:
        assert any(wave == w for w in waves)

def test_complex_wave_play():
    s1 = noise.SimpleWave(100, 1, 0.7)
    s2 = noise.SimpleWave(100, 1, 1)
    c1 = noise.ComplexWave([s1, s2])
    assert c1.play().max() <= 1
    assert c1.play().min() >= -1

def test_complex_wave_get_duration():
    s1 = noise.SimpleWave(100, 0.8, 0.7)
    s2 = noise.SimpleWave(190, 0.8, 1)
    c1 = noise.ComplexWave([s1, s2])
    assert abs(c1.get_duration() - 0.8) < 0.0001

def test_complex_wave_simplify():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(101, 1, 1)
    s3 = noise.SimpleWave(100, 1, 1)
    s4 = noise.SimpleWave(100, 1, 0.5)
    simple_waves = [s1, s2, s3, s4]
    c1 = noise.ComplexWave(simple_waves)
    c1.simplify()
    assert c1.complexity() == 2

def test_note_add():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(101, 1, 1)
    n1 = noise.Note([s1, s2])
    n2 = noise.Note([s1])
    n3 = n1 + n2
    assert n3.get_waves() == n1.get_waves() + n2.get_waves()

def test_note_get_waves():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(101, 1, 1)
    n1 = noise.Note([s1, s2])
    assert n1.get_waves()[0] == s1
    assert n1.get_waves()[1] == s2

def test_note_get_duration():
    s1 = noise.SimpleWave(100, 1, 1)
    s2 = noise.SimpleWave(101, 1, 1)
    n1 = noise.Note([s1, s2])
    assert abs(n1.get_duration() - 2) < 0.0001

def test_note_play():
    s1 = noise.SimpleWave(100, 1, 0.5)
    s2 = noise.SimpleWave(101, 1, 1)
    n1 = noise.Note([s1, s2])
    assert n1.play().max() <= 1
    assert n1.play().min() >= -1

def test_note_change_amplitude():
    s1 = noise.SimpleWave(100, 1, 0.5)
    s2 = noise.SimpleWave(101, 1, 1)
    n1 = noise.Note([s1, s2])
    n1.amplitude = 0.5
    wave = n1.play()
    half_way = len(wave) // 2
    assert wave[:half_way-10].max() <= 0.25
    assert wave[half_way+10:].max() <= 0.5
    assert wave[:half_way-10].min() >= -0.25
    assert wave[half_way+10:].min() >= -0.5

def test_sawtooth_add():
    st1 = noise.SawtoothWave(100, 1, 1)
    st2 = noise.SawtoothWave(90, 0.8, 1)
    w1 = st1 + st2
    waves = w1.get_waves()
    assert isinstance(w1, noise.ComplexWave)
    for wave in st1.get_waves():
        assert any(wave == w for w in waves)
    for wave in st2.get_waves():
        assert any(wave == w for w in waves)

def test_sawtooth_complexity():
    st1 = noise.SawtoothWave(100, 1, 1)
    assert st1.complexity() == 10

def test_sawtooth_play():
    st1 = noise.SawtoothWave(100, 1, 1)
    assert st1.play().max() <= 1
    assert st1.play().min() >= -1

def test_sawtooth_get_duration():
    st1 = noise.SawtoothWave(500, 100, 1)
    assert abs(st1.get_duration() - 100) < 0.0001

def test_sawtooth_get_waves():
    st1 = noise.SawtoothWave(500, 100, 1)
    assert st1.get_waves() == st1.waves

def test_sawtooth_simplify():
    st1 = noise.SawtoothWave(500, 100, 1)
    st1.simplify()
    assert st1.complexity() == 10

def test_square_add():
    sq1 = noise.SquareWave(100, 1, 1)
    sq2 = noise.SquareWave(90, 0.8, 1)
    w1 = sq1 + sq2
    waves = w1.get_waves()
    assert isinstance(w1, noise.ComplexWave)
    for wave in sq1.get_waves():
        assert any(wave == w for w in waves)
    for wave in sq2.get_waves():
        assert any(wave == w for w in waves)

def test_square_complexity():
    sq1 = noise.SquareWave(100, 1, 1)
    assert sq1.complexity() == 10

def test_square_play():
    sq1 = noise.SquareWave(100, 1, 1)
    assert sq1.play().max() <= 1
    assert sq1.play().min() >= -1

def test_square_get_duration():
    st1 = noise.SquareWave(500, 100, 1)
    assert abs(st1.get_duration() - 100) < 0.0001

def test_square_simplify():
    sq1 = noise.SquareWave(500, 100, 1)
    sq1.simplify()
    assert sq1.complexity() == 10

def test_rest_add():
    r1 = noise.Rest(10)
    s1 = noise.SimpleWave(100, 10, 1)
    w1 = r1 + s1
    np.testing.assert_allclose(s1.play(), w1.play(), atol=0.0001)

def test_rest_complexity():
    r1 = noise.Rest(10)
    assert r1.complexity() > 0

def test_rest_play():
    r1 = noise.Rest(1)
    assert r1.play().max() == 0
    assert r1.play().min() == 0

def test_rest_get_waves():
    r1 = noise.Rest(1)
    assert all(w.play().max() == 0 for w in r1.get_waves())
    assert all(w.play().min() == 0 for w in r1.get_waves())

def test_rest_get_duration():
    r1 = noise.Rest(20)
    assert abs(r1.get_duration() - 20) < 0.0001

def test_rest_simplify():
    r1 = noise.Rest(10)
    r1.simplify()
    assert r1.complexity() == 1

def test_stutter_note_add():
    sn1 = noise.StutterNote(100, 1, 1)
    n1 = noise.Note([noise.SimpleWave(400, 1, 2)])
    n2 = sn1 + n1
    waves = n2.get_waves()
    assert waves[:-1] == sn1.get_waves()
    assert waves[-1:] == n1.get_waves()

def test_stutter_note_get_waves():
    sn1 = noise.StutterNote(100, 1, 1)
    waves = sn1.get_waves()
    for wave in waves:
        assert abs(wave.get_duration() - 1/40) < 0.0001
    if waves[0].play().max() == 0:
        sl = slice(None, None, 2)
    else:
        sl = slice(1, None, 2)
    for wave in waves[sl]:
        assert wave.play().max() == 0
        assert wave.play().min() == 0

def test_stutter_note_get_duration():
    sn1 = noise.StutterNote(100, 9.1, 1)
    assert abs(sn1.get_duration() - 9.1) < 0.0001

def test_stutter_note_play():
    sn1 = noise.StutterNote(100, 2, 0.5)
    sn1.amplitude = 0.1
    assert sn1.play().max() <= 0.1
    assert sn1.play().min() >= -0.1

def test_baliset_get_duration():
    b1 = noise.Baliset()
    b1.next_notes([("1:1", 1, 0.2), ("3:1", 1, 0.8)])
    assert abs(b1.get_duration() - 1) < 0.0001

def test_baliset_play():
    b1 = noise.Baliset()
    b1.next_notes([("1:1", 1, 0.2), ("2:1", 0.5, 0.8)])
    bwave = b1.play()
    wave1 = noise.SawtoothWave(196, 0.2, 1).play()
    wave2 = noise.SawtoothWave(392, 0.8, 0.5).play()
    np.testing.assert_allclose(bwave[:len(wave1)-10], wave1[:-10], atol=0.0001)
    np.testing.assert_allclose(bwave[-len(wave2)+10:], wave2[10:], atol=0.0001)

def test_holophonor_get_duration():
    h1 = noise.Holophonor()
    h1.next_notes([("1:1", 1, 0.2), ("3:1", 1, 0.8)])
    assert abs(h1.get_duration() - 1) < 0.0001

def test_holophonor_play():
    h1 = noise.Holophonor()
    h1.next_notes([("1:1", 1, 0.2), ("2:1", 0.5, 0.8)])
    hwave = h1.play()
    wave1 = noise.StutterNote(65, 0.2, 1).play()
    wave2 = noise.StutterNote(130, 0.8, 0.5).play()
    np.testing.assert_allclose(hwave[:len(wave1)-10], wave1[:-10], atol=0.0001)
    np.testing.assert_allclose(hwave[-len(wave2)+10:], wave2[10:], atol=0.0001)

def test_gaffophone_get_duration():
    g1 = noise.Gaffophone()
    g1.next_notes([("1:1", 1, 0.2), ("3:1", 1, 0.8)])
    assert abs(g1.get_duration() - 1) < 0.0001

def test_gaffophone_play():
    g1 = noise.Gaffophone()
    g1.next_notes([("1:1", 1, 1)])
    gwave = g1.play()
    w1 = noise.SquareWave(131, 1, 1) + noise.SquareWave(196, 1, 1)
    w2 = noise.SquareWave(131, 1, 1) + noise.SquareWave(197, 1, 1)
    assert np.allclose(gwave, w1.play(), atol=0.0001) or np.allclose(gwave, w2.play(), atol=0.0001)

if __name__ == '__main__':
    import pytest
    pytest.main(['testing_handout.py'])
