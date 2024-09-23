{% macro ref(slug) %}
    {%- set __slug = slug.replace('-','_') -%}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {%- if __blk.is_rendered -%}
            {{-__blk.name-}}~\ref{ {{- __slug -}} }
        {%- else -%}
            \textbf{RefMissingBlock({{slug}})}
        {%- endif -%}
    {%- else -%}
        \\textbf{RefInvalidSlug({{slug}})}
    {%- endif -%}
{% endmacro %}

{% macro ref_or_name(slug) %}
    {%- set __slug = slug.replace('-','_') -%}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {%- if __blk.is_rendered -%}
            {{-__blk.name-}}~\ref{ {{- __slug -}} }
        {%- else -%}
            {{ __blk.name }}
        {%- endif -%}
    {%- else -%}
        \textbf\{RefInvalidSlug({{slug}})\}
    {%- endif -%}
{% endmacro %}

{% macro render(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {{ render_block(slug) }}
    {%- else -%}
        Uh oh.
    {%- endif -%}
{% endmacro %}