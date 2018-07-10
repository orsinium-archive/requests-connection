from timeit import timeit
import numpy

pure = []
patched = []
for _ in range(200):
    try:
        pure.append(timeit(
            setup=(
                "from requests import Session\n"
                "sess = Session()\n"
            ),
            stmt=(
                "sess.get('https://httpbin.org/get')\n"
            ),
            number=1,
        ))

        patched.append(timeit(
            setup=(
                "from requests_connection import Session, Connection\n"
                "conn = Connection.https('httpbin.org')\n"
                "sess = Session(conn)\n"
                ),
            stmt=(
                "sess.get('https://httpbin.org/get')\n"
            ),
            number=1,
        ))
    except KeyboardInterrupt:
        break


count = min([len(pure), len(patched)])
pure = min(pure), sum(pure) / len(pure), max(pure)
patched = min(patched), sum(patched) / len(patched), max(patched)


print('Requests: {:.03} ± {:.4}'.format(
    numpy.mean(pure),
    numpy.std(pure),
))
print('Patched:  {:.03} ± {:.4}'.format(
    numpy.mean(patched),
    numpy.std(patched),
))

print('Runs: ', count)
