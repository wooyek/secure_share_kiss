To run this example, please call:

    docker-compose build
    docker-compose up
    
To test this example please run:
        
    cd secure_share_kiss
    pew new -p python3 -a $(pwd) $(pwd | xargs basename)
    pip install -e .
    env DJANGO_SETTINGS_MODULE=secure_share_kiss.settings_dev python manage.py collectstatic
    pytest