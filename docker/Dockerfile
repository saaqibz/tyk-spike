FROM tykio/tyk-host-manager
# Add cors.conf
RUN wget https://gist.githubusercontent.com/Stanback/7145487/raw/73a66246a72d3bdb5e025fda101f13bb82e87904/nginx.conf
RUN mv nginx.conf /etc/nginx/conf.d/cors.conf

# Start the host manager
CMD ["/opt/tyk-dashboard/host-manager/entrypoint.sh"]
