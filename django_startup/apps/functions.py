import os


def setup_authentication_serializer_py(project_name):
    serializer_file = os.path.join(project_name, "authentication", "serializers.py")
    if not os.path.exists(serializer_file):
        with open(serializer_file, "w") as f:
            f.write("")

    with open(serializer_file, "r") as f:
        content = f.read()

    content = "from rest_framework import serializers\n" + content

    user_serializer_code = f"""class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'"""

    # Append model code at end
    content = content.rstrip()  # Remove trailing spaces/new lines
    content += "\n" + user_serializer_code.lstrip()  # Ensure proper alignment

    # Write back to models.py
    with open(serializer_file, "w") as f:
        f.write(content)


def add_authentication_view_functions(project_name):
    views_file = os.path.join(project_name, "authentication", "views.py")
    register_code = \
        f"""@api_view([POST])
            def register_view(request):
                pass"""

    with open(views_file, "r") as f:
        content = f.read()

    # Append model code at end
    content = content.rstrip()  # Remove trailing spaces/new lines
    content += "\n" + register_code.lstrip()  # Ensure proper alignment

    # Write back to models.py
    with open(views_file, "w") as f:
        f.write(content)