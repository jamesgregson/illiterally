{% macro ref(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {%- if __blk.is_rendered -%}
            {{__blk.name}}
        {%- else -%}
            RefMissingBlock({{__blk.slug}})
        {%- endif -%}
    {%- else -%}
        RefInvalidSlug({{slug}})
    {%- endif -%}
{% endmacro %}

{% macro ref_or_name(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {{__blk.name}}
    {%- else -%}
        RefInvalidSlug({{slug}})
    {%- endif -%}
{% endmacro %}

{% macro render(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {{ render_block(slug) }}
    {%- else -%}
        RenderInvalidSlug({{slug}})
    {%- endif -%}
{% endmacro %}