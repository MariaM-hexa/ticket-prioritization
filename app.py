from flask import Flask, render_template, request, jsonify
 
app = Flask(__name__)
 
# Simulación de agentes con especialidades y cargas de trabajo
agents = [
    {"id": 1, "name": "Agent A", "expertise": ["network", "hardware"], "load": 2},
    {"id": 2, "name": "Agent B", "expertise": ["software", "database"], "load": 1},
    {"id": 3, "name": "Agent C", "expertise": ["hardware", "software"], "load": 3},
]
 
# Función simple para analizar texto y asignar prioridad
def analyze_ticket(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["urgent", "immediately", "down", "failure"]):
        priority = "High"
    elif any(word in text_lower for word in ["slow", "issue", "error"]):
        priority = "Medium"
    else:
        priority = "Low"
    # Categoría basada en palabras clave simples
    if "network" in text_lower:
        category = "network"
    elif "hardware" in text_lower:
        category = "hardware"
    elif "software" in text_lower:
        category = "software"
    else:
        category = "general"
    return priority, category
 
# Función para asignar agente basado en categoría y carga menor
def assign_agent(category):
    suitable_agents = [agent for agent in agents if category in agent["expertise"]]
    if not suitable_agents:
        suitable_agents = agents  # Si no hay especialista, asignar cualquiera
    # Ordenar por carga y seleccionar el de menor carga
    suitable_agents.sort(key=lambda x: x["load"])
    assigned_agent = suitable_agents[0]
    assigned_agent["load"] += 1  # Incrementar carga
    return assigned_agent
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    data = request.json
    description = data.get("description", "")
    if not description.strip():
        return jsonify({"error": "Ticket description cannot be empty."}), 400
 
    priority, category = analyze_ticket(description)
    agent = assign_agent(category)
 
    ticket = {
        "description": description,
        "priority": priority,
        "category": category,
        "assigned_agent": agent["name"]
    }
    return jsonify(ticket)
 
if __name__ == '__main__':
    app.run(debug=True)