from flask import Flask, request, jsonify, render_template, send_file
from services.excel_service import load_menu_data, filter_menu
from services.menu_builder import calculate_menu_price
from services.email_service import send_email
from services.pdf_generator import generate_pdf
import os
from dotenv import load_dotenv
from openai import OpenAI  # ✅ NEW OpenAI Client

# Load environment variables
load_dotenv()

# Load and print keys
api_key = os.getenv("OPENAI_API_KEY")
print("API Key Loaded:", api_key)
print("Commercial Email Loaded:", os.getenv("COMMERCIAL_EMAIL"))
print("Email User Loaded:", os.getenv("EMAIL_USER"))

# ✅ Initialize OpenAI client
client = OpenAI(api_key=api_key)

COMMERCIAL_EMAIL = os.getenv("COMMERCIAL_EMAIL")

app = Flask(__name__)

# 🔹 0. Root
@app.route('/')
def index():
    return render_template('chatbot.html')


# 🔹 1. Chatbot route
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    system_prompt = """
    Eres un asistente comercial que ayuda a los clientes a diseñar presupuestos de menú de boda. 
    Primero, pregúntales por su preferencia de opción gastronómica. Las opciones son:
    1. Alquimia
    2. Chas
    Luego, pregunta cuántos invitados tendrán y si el evento será de día o noche.
    Asegúrate de ofrecer los precios sin mostrar los detalles individuales de los platos.
    """

    # ✅ Correct usage of OpenAI v1+
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})


# 🔹 2. Price calculator
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    df = load_menu_data()
    filtered = filter_menu(df, data['gastronomic_type'])

    selected_items = []
    for _, row in filtered.iterrows():
        if row['Nombre'] in data['selected_items']:
            selected_items.append(row.to_dict())

    price_per_guest, total = calculate_menu_price(
        selected_items,
        data['guests'],
        data['gastronomic_type'],
        data['time_of_day']
    )

    return jsonify({
        "price_per_guest": price_per_guest,
        "total_price": total
    })


# 🔹 3. Send PDF proposal
@app.route('/api/send-proposal', methods=['POST'])
def send_proposal():
    data = request.json
    html = render_template("proposal.html", **data)
    pdf_path = generate_pdf(html)

    send_email(data['email'], "Tu propuesta de menú para la boda", html)

    return send_file(pdf_path, as_attachment=True)


# 🔹 4. Confirm with commercial team
@app.route('/api/confirm-proposal', methods=['POST'])
def confirm_proposal():
    data = request.json  # contains name, email, phone, proposals (list of dicts)

    proposals_html = ""
    for i, prop in enumerate(data['proposals']):
        proposals_html += f"<h4>Propuesta {i+1}</h4>"
        proposals_html += f"<p>Opción: {prop['gastronomic_type']} | Invitados: {prop['guests']} | Horario: {prop['time_of_day']}</p>"
        proposals_html += f"<p>Menú: {', '.join(prop['selected_items'])}</p>"
        proposals_html += f"<p><strong>Precio final:</strong> {prop['total_price']} €</p><hr>"

    full_message = f"""
    <h3>Nuevo cliente interesado</h3>
    <p><strong>Nombre:</strong> {data['name']}</p>
    <p><strong>Email:</strong> {data['email']}</p>
    <p><strong>Teléfono:</strong> {data['phone']}</p>
    {proposals_html}
    """

    send_email(COMMERCIAL_EMAIL, "Nueva propuesta confirmada desde el chatbot", full_message)

    return jsonify({
        "message": "Propuesta enviada al departamento comercial. Puedes contactarles al +34 655953034"
    })


if __name__ == '__main__':
    app.run(debug=True)




'''from flask import Flask, request, jsonify, render_template, send_file
from services.excel_service import load_menu_data, filter_menu
from services.menu_builder import calculate_menu_price
from services.email_service import send_email
from services.pdf_generator import generate_pdf
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

print("API Key Loaded:", os.getenv("OPENAI_API_KEY"))
print("Commercial Email Loaded:", os.getenv("COMMERCIAL_EMAIL"))
print("Email User Loaded:", os.getenv("EMAIL_USER"))
load_dotenv()
app = Flask(__name__)

# Load API keys
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
COMMERCIAL_EMAIL = os.getenv("COMMERCIAL_EMAIL")


@app.route('/')
def index():
    return render_template('chatbot.html')

# 🔹 1. OpenAI chatbot route
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Step-by-step menu selection
    system_prompt = """
    Eres un asistente comercial que ayuda a los clientes a diseñar presupuestos de menú de boda. 
    Primero, pregúntales por su preferencia de opción gastronómica. Las opciones son:
    1. Alquimia
    2. Chas
    Luego, pregunta cuántos invitados tendrán y si el evento será de día o noche.
    Asegúrate de ofrecer los precios sin mostrar los detalles individuales de los platos.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

# 🔹 2. Calculate price from selected menu
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    df = load_menu_data()
    filtered = filter_menu(df, data['gastronomic_type'])
    
    selected_items = []
    for _, row in filtered.iterrows():
        if row['Nombre'] in data['selected_items']:
            selected_items.append(row.to_dict())

    price_per_guest, total = calculate_menu_price(
        selected_items,
        data['guests'],
        data['gastronomic_type'],
        data['time_of_day']
    )

    return jsonify({
        "price_per_guest": price_per_guest,
        "total_price": total
    })


# 🔹 3. Send proposal PDF to client
@app.route('/api/send-proposal', methods=['POST'])
def send_proposal():
    data = request.json
    html = render_template("proposal.html", **data)
    pdf_path = generate_pdf(html)

    # Send email to client
    send_email(data['email'], "Tu propuesta de menú para la boda", html)

    return send_file(pdf_path, as_attachment=True)


# 🔹 4. Confirm with commercial team
@app.route('/api/confirm-proposal', methods=['POST'])
def confirm_proposal():
    data = request.json  # contains: name, email, phone, proposals (list of dicts)

    proposals_html = ""
    for i, prop in enumerate(data['proposals']):
        proposals_html += f"<h4>Propuesta {i+1}</h4>"
        proposals_html += f"<p>Opción: {prop['gastronomic_type']} | Invitados: {prop['guests']} | Horario: {prop['time_of_day']}</p>"
        proposals_html += f"<p>Menú: {', '.join(prop['selected_items'])}</p>"
        proposals_html += f"<p><strong>Precio final:</strong> {prop['total_price']} €</p><hr>"

    full_message = f"""
    <h3>Nuevo cliente interesado</h3>
    <p><strong>Nombre:</strong> {data['name']}</p>
    <p><strong>Email:</strong> {data['email']}</p>
    <p><strong>Teléfono:</strong> {data['phone']}</p>
    {proposals_html}
    """

    send_email(COMMERCIAL_EMAIL, "Nueva propuesta confirmada desde el chatbot", full_message)

    return jsonify({
        "message": "Propuesta enviada al departamento comercial. Puedes contactarles al +34 655953034"
    })


if __name__ == '__main__':
    app.run(debug=True)'''
