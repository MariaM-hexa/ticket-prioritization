import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
 
# Cargar variables de entorno desde .env
load_dotenv()
 
app = Flask(__name__)
 
# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
 
# Simulación de agentes con especialidades y cargas de trabajo
agents = [
    {"id": 1, "name": "Agent A", "expertise": ["network", "hardware"], "load": 2},
    {"id": 2, "name": "Agent B", "expertise": ["software", "database"], "load": 1},
    {"id": 3, "name": "Agent C", "expertise": ["hardware", "software"], "load": 3},
]
 
def analyze_ticket(text):
    """
    Analiza el texto del ticket para determinar prioridad y categoría.
    Usa reglas simples como simulación de IA generativa.
    """
    logging.info("Analyzing ticket text.")
    text_lower = text.lower()
    if any(word in text_lower for word in ["urgent", "immediately", "down", "failure"]):
        priority = "High"
    elif any(word in text_lower for word in ["slow", "issue", "error"]):
        priority = "Medium"
    else:
        priority = "Low"
 
    if "network" in text_lower:
        category = "network"
    elif "hardware" in text_lower:
        category = "hardware"
    elif "software" in text_lower:
        category = "software"
    else:
        category = "general"
 
    logging.info(f"Ticket assigned priority '{priority}' and category '{category}'.")
    return priority, category
 
def assign_agent(category):
    """
    Asigna un agente basado en la categoría y carga actual menor.
    """
    logging.info(f"Assigning agent for category '{category}'.")
    suitable_agents = [agent for agent in agents if category in agent["expertise"]]
    if not suitable_agents:
        suitable_agents = agents  # Asignar cualquiera si no hay especialista
 
    suitable_agents.sort(key=lambda x: x["load"])
    assigned_agent = suitable_agents[0]
    assigned_agent["load"] += 1  # Incrementar carga
    logging.info(f"Assigned agent: {assigned_agent['name']} (new load: {assigned_agent['load']})")
    return assigned_agent
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    data = request.json
    description = data.get("description", "").strip()
    if not description:
        logging.warning("Received empty ticket description.")
        return jsonify({"error": "Ticket description cannot be empty."}), 400
 
    try:
        priority, category = analyze_ticket(description)
        agent = assign_agent(category)
 
        ticket = {
            "description": description,
            "priority": priority,
            "category": category,
            "assigned_agent": agent["name"]
        }
        logging.info(f"Ticket processed successfully: {ticket}")
        return jsonify(ticket)
    except Exception as e:
        logging.error(f"Error processing ticket: {e}")
        return jsonify({"error": "Internal server error"}), 500
 
if __name__ == '__main__':
    app.run(debug=True)