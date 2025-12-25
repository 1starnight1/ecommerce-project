from app import create_app
from flask import url_for

app = create_app()

with app.test_request_context():
    print("Testing URL generation for add_to_cart...")
    try:
        url = url_for('cart.add_to_cart', product_id=1)
        print(f"URL generated successfully: {url}")
    except Exception as e:
        print(f"Error generating URL: {e}")

    print("\nAll registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule}")
