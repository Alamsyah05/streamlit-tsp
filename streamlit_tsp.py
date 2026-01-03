import streamlit as st
import pulp as lp
import pandas as pd

st.title("Aplikasi Optimasi TSP gacor")

kota = ['blitar', 'malang', 'surabaya', 'pasuruan', 'batu']
jarak = {('blitar', 'blitar'): 0, ('blitar', 'malang'): 70, ('blitar', 'surabaya'): 180, ('blitar', 'pasuruan'): 130, ('blitar', 'batu'): 75,
         ('malang', 'blitar'): 70, ('malang', 'malang'): 0, ('malang', 'surabaya'): 90, ('malang', 'pasuruan'): 50, ('malang', 'batu'): 20,
         ('surabaya', 'blitar'): 180, ('surabaya', 'malang'): 90, ('surabaya', 'surabaya'): 0, ('surabaya', 'pasuruan'): 70, ('surabaya', 'batu'): 110,
         ('pasuruan', 'blitar'): 130, ('pasuruan', 'malang'): 50, ('pasuruan', 'surabaya'): 70, ('pasuruan', 'pasuruan'): 0, ('pasuruan', 'batu'): 65,
         ('batu', 'blitar'): 75, ('batu', 'malang'): 20, ('batu', 'surabaya'): 110, ('batu', 'pasuruan'): 65, ('batu', 'batu'): 0
         }

# Buat DataFrame matriks
df_jarak = pd.DataFrame(index=kota, columns=kota)

for (i, j), d in jarak.items():
    df_jarak.loc[i, j] = d

df_jarak = df_jarak.astype(int)

st.header("Matriks Jarak Antar Kota")
st.dataframe(df_jarak)

btn_hitung = st.button("click me")

if btn_hitung:
    problem = lp.LpProblem("TSP", lp.LpMinimize)

    rute = lp.LpVariable.dicts('rute', jarak, 0, 1, lp.LpBinary)
    urutan = lp.LpVariable.dicts('urutan', kota, 0, len(kota)-1, lp.LpInteger)

    problem += lp.lpSum([jarak[(i, j)] * rute[(i, j)]
                        for i in kota for j in kota if i != j])

    for k in kota:
        problem += lp.lpSum([rute[(k, j)] for j in kota if j != k]) == 1, f"Ke_{k}"
        problem += lp.lpSum([rute[(i, k)]
                            for i in kota if i != k]) == 1, f"Dari_{k}"

    n = len(kota)

    for i in kota:
        for j in kota:
            if i != j and (i != 'blitar' and j != 'blitar'):
                problem += urutan[i] - urutan[j] + n * rute[(i, j)] <= n-1

    problem.writeLP("Permasalahan_TSP")
    status = problem.solve()

    # print("Status :", lp.LpStatus[status])
    st.text(f"Status : {lp.LpStatus[status]}")

    for i in problem.variables():
        # print(i.name, ":", i.varValue)
        st.text(f"{i.name} : {i.varValue}")

    # print("Total Jarak :", lp.value(problem.objective))
    st.text(f"Total Jarak : {lp.value(problem.objective)}")