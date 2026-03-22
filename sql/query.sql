{% for value in params.data %}
SELECT {{ value }} AS id
{% if not loop.last %}
UNION ALL
{% endif %}{% endfor %}