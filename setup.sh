
echo ""
echo "  ██████╗  █████╗ ██████╗ ██╗  ██╗███╗   ███╗ █████╗ ████████╗████████╗███████╗██████╗ "
echo "  ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝████╗ ████║██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗"
echo "  ██║  ██║███████║██████╔╝█████╔╝ ██╔████╔██║███████║   ██║      ██║   █████╗  ██████╔╝"
echo "  ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║╚██╔╝██║██╔══██║   ██║      ██║   ██╔══╝  ██╔══██╗"
echo "  ██████╔╝██║  ██║██║  ██║██║  ██╗██║ ╚═╝ ██║██║  ██║   ██║      ██║   ███████╗██║  ██║"
echo "  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝"
echo ""
echo "  Engineering Beyond Boundaries"
echo "  ─────────────────────────────"
echo ""

# Check Python
python3 --version || { echo "ERROR: Python 3 not found"; exit 1; }

echo "[2/4] Running migrations..."
python3 manage.py migrate
echo "[4/4] Collecting static files..."
python3 manage.py collectstatic --noinput

echo ""
echo "  ✅ Setup complete!"
echo ""
echo "  Run the server:"
echo "  python3 manage.py runserver"
echo ""
echo "  Access:"
echo "  → Website:    http://127.0.0.1:8000/"
echo "  → Admin:      http://127.0.0.1:8000/admin/"
echo ""
