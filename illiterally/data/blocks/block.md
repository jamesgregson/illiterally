{%- import 'macros.md.inc' as macros with context -%}
{%- set __blk = block(slug) -%}
#### <a name="{{__blk.slug}}"></a>{{__blk.left}}**{{__blk.name}}**{{__blk.right}}: [{{source_url(__blk.filename,__file__)}}: {{__blk.line}}]({{source_url(__blk.filename,__file__)}})
___
```python
{{__blk.text}}
```
{% if __blk.parent -%}
    <span>
        {%- for comp in __blk.path -%}
            {%- if comp != __blk.slug -%}
                {{ macros.ref_or_name(comp) }} |&nbsp;
            {%- else -%}
                {{ __blk.name }}
            {%- endif -%}
        {%- endfor -%}
    </span>
{%- endif %}
{% for cref in __blk.nested %}
{%- set child = block(cref) -%}
{%- if child and child.is_rendered -%}
- {{ macros.ref_or_name(cref) }}
{% endif -%}
{% endfor %}
___