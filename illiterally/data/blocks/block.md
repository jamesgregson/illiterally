#### <a name="{{block.slug}}"></a>{{block.left}}**{{block.name}}**{{block.right}}: [{%raw%}{{SRC_PATH}}{%endraw%}: {{block.line}}]({%raw%}{{SRC_PATH}}{%endraw%})
___
```python
{{block.text}}
```

{% if block.parent -%}
    <span>
        {%- for comp in block.path -%}
            {%- if blocks[comp].is_rendered and blocks[comp].slug != block.slug -%}
                [{{blocks[comp].name}}](#{{comp}})
            {%- else -%}
                {{blocks[comp].name}}
            {%- endif -%}
            {%- if comp != block.slug %} | {% endif -%}
        {%- endfor -%}
    </span>
{%- endif %}
{% for ref in block.nested %}
- {% if blocks[ref].is_rendered %}[{{blocks[ref].name}}](#{{ref}}){% else %}{{blocks[ref].name}}{%endif%}
{% endfor %}
___