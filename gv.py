from graphviz import Digraph

# Function to save and render diagrams
def render_diagram(dot, filename):
    dot.render(filename, format='png', cleanup=True)

# 1. Entity-Relationship (ER) Diagram
def create_er_diagram():
    dot = Digraph(comment='ER Diagram for Herbal Leaf Identification')
    dot.attr(rankdir='TB')

    # Entities
    dot.node('U', 'User\n(id, username, password, email)', shape='record')
    dot.node('LI', 'LeafImage\n(image_id, filename, leaf_type)', shape='record')
    dot.node('HI', 'HerbInfo\n(herb_id, name, benefits)', shape='record')
    dot.node('P', 'Prediction\n(prediction_id, leaf_type, confidence)', shape='record')

    # Relationships
    dot.edge('U', 'LI', label='Uploads')
    dot.edge('LI', 'P', label='Generates')
    dot.edge('P', 'HI', label='Links To')
    dot.edge('U', 'P', label='Views')

    render_diagram(dot, 'er_diagram_herbal')

# 2. Data Flow Diagram (DFD)
def create_dfd():
    dot = Digraph(comment='Data Flow Diagram for Herbal Leaf Identification')
    dot.attr(rankdir='LR')

    # External Entities
    dot.node('U', 'User', shape='ellipse')
    dot.node('A', 'Admin', shape='ellipse')

    # Processes
    dot.node('P1', '1. Authenticate User', shape='circle')
    dot.node('P2', '2. Upload Image', shape='circle')
    dot.node('P3', '3. Process Image', shape='circle')
    dot.node('P4', '4. Classify Leaf', shape='circle')
    dot.node('P5', '5. Retrieve Info', shape='circle')
    dot.node('P6', '6. Manage Users', shape='circle')

    # Data Stores
    dot.node('D1', 'User Data', shape='cylinder')
    dot.node('D2', 'Leaf Images', shape='cylinder')
    dot.node('D3', 'Predictions', shape='cylinder')
    dot.node('D4', 'Herb Database', shape='cylinder')

    # Data Flows
    dot.edge('U', 'P1', label='Signup/Login')
    dot.edge('P1', 'D1', label='Store User')
    dot.edge('D1', 'P1', label='Verify/OTP')
    dot.edge('U', 'P2', label='Upload Image')
    dot.edge('P2', 'D2', label='Store Image')
    dot.edge('D2', 'P3', label='Fetch Image')
    dot.edge('P3', 'P4', label='Processed Image')
    dot.edge('P4', 'D3', label='Prediction')
    dot.edge('D3', 'P5', label='Leaf Type')
    dot.edge('P5', 'D4', label='Query Info')
    dot.edge('D4', 'P5', label='Herb Details')
    dot.edge('P5', 'U', label='Display Results')
    dot.edge('A', 'P6', label='Manage Request')
    dot.edge('P6', 'D1', label='User List')
    dot.edge('D1', 'P6', label='User Info')

    render_diagram(dot, 'dfd_herbal')

# 3. Block Diagram
def create_block_diagram():
    dot = Digraph(comment='Block Diagram for Herbal Leaf Identification')
    dot.attr(rankdir='TB')

    # Blocks
    dot.node('UI', 'User Interface\n(templates/*.html)', shape='box')
    dot.node('AUTH', 'Authentication Module\n(app.py)', shape='box')
    dot.node('UPLOAD', 'Image Upload Module\n(app.py, app0.py)', shape='box')
    dot.node('PROC', 'Image Processing\n(app0.py)', shape='box')
    dot.node('ML', 'Classification Model\n(herbal_leaf_classifier.h5, train_mode.py)', shape='box')
    dot.node('INFO', 'Herb Info Module\n(app.py)', shape='box')
    dot.node('ADMIN', 'Admin Dashboard\n(app.py)', shape='box')
    dot.node('STORE', 'Storage\n(instance/*.db, uploads, Segmented_Medicinal_Leaf_Images)', shape='box')

    # Connections
    dot.edge('UI', 'AUTH', label='Credentials/OTP')
    dot.edge('AUTH', 'STORE', label='Store/Verify')
    dot.edge('UI', 'UPLOAD', label='Upload Image')
    dot.edge('UPLOAD', 'STORE', label='Save Image')
    dot.edge('STORE', 'PROC', label='Raw Image')
    dot.edge('PROC', 'ML', label='Processed Image')
    dot.edge('ML', 'INFO', label='Prediction')
    dot.edge('INFO', 'UI', label='Herb Details')
    dot.edge('ADMIN', 'STORE', label='Manage Users')
    dot.edge('STORE', 'UI', label='User Data')

    render_diagram(dot, 'block_diagram_herbal')

# Generate all diagrams
create_er_diagram()
create_dfd()
create_block_diagram()

print("Diagrams generated: er_diagram_herbal.png, dfd_herbal.png, block_diagram_herbal.png")