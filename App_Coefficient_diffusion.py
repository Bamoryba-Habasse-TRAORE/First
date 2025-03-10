from flask import Flask, request, redirect, url_for, render_template_string
import numpy as np

app = Flask(__name__)

def calculate_diffusion_coefficient(xA, D_AB_exp):
    try:
        if not (0 <= xA <= 1):
            raise ValueError("xA doit être compris entre 0 et 1.")
        if D_AB_exp <= 0:
            raise ValueError("D_AB_exp doit être un nombre positif.")
        
        xB = 1 - xA
        aBA, aAB = 194.5302, -10.7575
        rA, rB = 1.4311, 0.92
        phiA, phiB = 0.279, 0.746
        thetaAB, thetaBA, thetaAA, thetaBB = 0.261, 0.612, 0.388, 0.739
        tauAB = np.exp(-aAB / 313.13)
        tauBA = np.exp(-aBA / 313.13)
        D_AB_pur, D_BA_pur = 2.1E-5, 2.67E-5
        
        A = xB * np.log(D_AB_pur) + xA * np.log(D_BA_pur)
        B = xA * xB
        C = (phiA / xA) * (1 - (rA**(1/3) / rB**(1/3))) if xA != 0 else 0
        D = (phiB / xB) * (1 - (rB**(1/3) / rA**(1/3))) if xB != 0 else 0
        E, H = xB * 1.432, xA * 1.4
        F, G = (1 - thetaBA**2) * np.log(tauBA), (1 - thetaBB**2) * tauAB * np.log(tauAB)
        I, J = (1 - thetaAB**2) * np.log(tauAB), (1 - thetaAA**2) * tauBA * np.log(tauBA)
        K = xA * np.log(xA / phiA) if xA != 0 else 0
        L = xB * np.log(xB / phiB) if xB != 0 else 0
        
        ln_D_AB = A + (2 * B * (C + D)) + E * (F + G) + H * (I + J) + (2 * (K + L))
        D_AB = np.exp(ln_D_AB)
        error = abs((D_AB_exp - D_AB) / D_AB_exp) * 100

        return D_AB, error
    except Exception as e:
        return str(e), None  

@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome</h1>
        <h2>Calcul du coefficient de diffusion</h2>
        <a href='/calcul'><button>Aller au calcul</button></a>
        <details>
                <summary> Objectif Application </summary>
               <p> Cette application a pour objectif d'estimer le coefficient de diffusion en utilisant le modèle UNIFAC et aussi trouver l'erreur relative .</p>
               <p> Bon Usage &#128512 ! </p>
        </details> 
    ''')

@app.route('/calcul', methods=['GET', 'POST'])
def calcul():
    if request.method == 'POST':
        try:
            xA = float(request.form['x_A'].strip().replace(",", "."))
            D_AB_exp = float(request.form['D_exp'].strip().replace(",", "."))
        except ValueError:
            return render_template_string('<h3>Valeur incorrecte, veuillez entrer des nombres valides.</h3> <a href="http://127.0.0.1:9999/calcul">Retour</a>')
        
        return redirect(url_for('resultat', xA=xA, D_AB_exp=D_AB_exp))
    
    return render_template_string('''
        <h2>Veuillez fournir ces données</h2>
        <form method='post'>
            x_A: <input type='text' name='x_A'><br>
            D_exp: <input type='text' name='D_exp'><br>
            <input type='submit' value='Calculer'>
        </form>
    ''')

@app.route('/resultat')
def resultat():
    try:
        xA = float(request.args['xA'])
        D_AB_exp = float(request.args['D_AB_exp'])
        
        D_AB, error = calculate_diffusion_coefficient(xA, D_AB_exp)
        
        if isinstance(D_AB, str):  # Si c'est un message d'erreur
            return render_template_string(f'<h3>Erreur : {D_AB}</h3>')
        
        result_message = f"Coefficient de diffusion D_AB : {D_AB:.4e} cm²/s  Erreur : {error:.2f}%"
        return render_template_string('''
            <h3>Résultat du Calcul</h3>
            <p>{{ result_message }}</p>
            <a href='/calcul'><button>Recommencer</button></a>
            <a href='/'><button>Accueil</button></a>
        ''', result_message=result_message)
    except Exception as e:
        return render_template_string(f'<h3>Erreur lors du calcul : {str(e)}</h3>')


@app.errorhandler(500)
def page_not_found(error):
    return render_template_string('<h3>Page non trouvée</h3>'), 500

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=9999)
