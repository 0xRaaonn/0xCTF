import time

limit = 0xe5db6a6d765b1ba6e727aa7a87a792c49bb9ddeb2bad999f5ea04f047255d5a72e193a7d58aa8ef619b0262de6d25651085842fd9c385fa4f1032c305f44b8a4f92b16c8115d0595cebfccc1c655ca20db597ff1f01e0db70b9073fbaa1ae5e489484c7a45c215ea02db3c77f1865e1e8597cb0b0af3241cd8214bd5b5c1491f

def walking(x, y, part):
    epart = [int.from_bytes(part[i:i+2], "big") for i in range(0, 8, 2)]
    xx = epart[0] * x + epart[1] * y
    yy = epart[2] * x + epart[3] * y
    return xx, yy

def dfs(x, y, target_x, target_y, chunks, used, path, depth, max_depth, start_time, time_limit=60, memo=None):
    if memo is None:
        memo = set()
    if time.time() - start_time > time_limit:
        return None
    if depth > max_depth:
        return None

    # State pruning memoization
    state = (x, y, depth)
    if state in memo:
        return None
    memo.add(state)

    # If out of bounds, mod and check if equals target
    if x > limit or y > limit:
        x %= limit
        y %= limit
        if (x, y) == (target_x, target_y):
            return path
        else:
            return None

    # If matched target with some steps taken
    if (x, y) == (target_x, target_y) and depth > 0:
        return path

    # Try all unused chunks
    for i, chunk in enumerate(chunks):
        if i in used:
            continue
        xx, yy = walking(x, y, chunk)
        used.add(i)
        res = dfs(xx, yy, target_x, target_y, chunks, used, path + [chunk], depth + 1, max_depth, start_time, time_limit, memo)
        used.remove(i)
        if res is not None:
            return res

    return None

if __name__ == "__main__":
    # Fill in these from your output:
    x0 = 81831414834740272074928093109593882161315066576968785965890012410682648935690
    y0 = 6284279319053449749834193096144375467836588735432227100196581742365460275073

    xf = 998865837243708443337438363430163285684308148911558504363745541135627933996750539197753084673110872924401325348627821800612869293715450205483786012882691144562729381376575632811054866418253286192400587037567550669101312
    yf = 10834466466263164263303604217368393986695017433792722494119390610480133517007944122477085145760302725744619201061161139181200469687911813309302079660840262721652823622795391813477492418631369412149751402032808180601576448

    mind_hex = "bd38b38df431d852c689295727cd43ab28b8019c08093cf2dd77ae3561c106de7a231b69fbfd80ae545a8cbe0997096aba2395d1db51e26504b507142a3d50990c03516d2b02ab78cdfbef872f407de100588f761b562fa6a8a800b84ecfcdad3fce80c249866c5b81778c275c69487c91423bb1712308c362ef19169c4fd2b870c64b43cdce384330e0473fb2c6ecc834688cd770fac0a7359cc798e398dbab0fb7e161a8b8299d024544ebeb9b8b273dc4e1c1d239963e3633fdc2eae5b5fc64785454abf4504e313cf8fefdab7756dcc2feb266c14e6d1df71560c662fd7f90046317e03990ec81d942664f0379a57dca37680c43a7de432b754edebcb7d2c9ffc0923a422f8d54009af0517b1e99055799db8595f5df3c1c08436067b8f1f7d5be91ab64c069b049b9d405ac6f743333dd66b91d49c2291d09bb9a6adc956efa6d2f763c5faa84f6fa85849c945635d0aa83067ae04cee24f8440ac7833ed368e5ff7878b967179a6958573110ccc80eb51bcee1bbeddd208b0f28712b306731d74c486cdcdac82e81396cc7e4f173694ced549a57a47813c0489c8b693a5a62e5e1889adee5f6f87a5cc5146e2f02fd18dbe114f0624ef341e00e74142a853238da37d9c2eeec01ccc53d44376cdd676407c36ae0023c79ae270b37b264992ce919021c699d5b861ce3dbbfa2b269dcf71556142ba53785546dda45ee5604807b11bd4ccfbf5e98b9afb0836b3af1b3d9f9482809ce5778a5bba6428f3884f6b2a8ffb0ef5e1a350c2c3ae5b0292f59c56f7049389c195a143f710c01341a990c3d2c3121bf003614ce3b1c9d58c4a7de220b1dd03a73e05a25f3a18ff02994394c54e85c868e9a1cffd490f8502ac921d18e54cd89484f5623f9b8eaa930051ceba05c95c9db5ebc5763826050f677becff200a10d63bdf567ee0d1e9da856e2c42fe0bdb8a75c518d6ca9bf833b8fed3a08eeda9a6940c0d37dcfa02706b92894a0a9cc782d0477490a54a325bbdefef1aef89a1ef8b13e8664f26fd4c9afada5eeaa3282814b1a3c96e4a347b73f3e4354cb9a808ccaa8b2d24a31d825922a4607b686005ba29eb69b35c18607f2b2851662457fc6d6efd47c8bfc62646de36e623f156a86710c4be68ea4ddebcb2d104d4012838e458386c4545796a76fc9b753a5b6caf924b73b1616119e7f5fed7d0f7f226e1a79e8940bfc84a50b9d8b1b0bdd70ca668dc2ddc01589ff811e86a4d08611e8e9b8ac04b71741e0b0e844e655c40be02a670eebcffe07af7db6524a4b9fd8faf6844027980af72aa38928dcff987c649e12dfe1aeb7bdee27e5b95c4fbb01c279e543ca85521087a57c94bbaabf19059ff842db3033e24e4265be1df532d7c7d93f704505473a0178bb0c69dbae3f80"

    mind_chunks = [bytes.fromhex(mind_hex[i:i+16]) for i in range(0, len(mind_hex), 16)]

    print("Starting DFS search for path...")
    path = dfs(x0, y0, xf, yf, mind_chunks, set(), [], 0, 30, time.time(), time_limit=300)  # 5 min time limit

    if path is None:
        print("No valid path found within time and depth limits.")
    else:
        print(f"Found path with {len(path)} steps:")
        path_hex = ''.join(chunk.hex() for chunk in path)
        print(path_hex)

        # Verification
        pos = (x0, y0)
        for chunk in path:
            pos = walking(pos[0], pos[1], chunk)
        pos = (pos[0] % limit, pos[1] % limit) if pos[0] > limit or pos[1] > limit else pos
        if pos == (xf, yf):
            print("Verification succeeded: final position matches!")
        else:
            print("Verification failed: final position mismatch.")
