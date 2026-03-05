import os

xml_content = """<mxfile host="Electron" type="device">
  <diagram id="pipeline_arch" name="End-to-End Pipeline">
    <mxGraphModel dx="1000" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Nodes -->
        <mxCell id="2" value="Google BigQuery&#10;(Source Data)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="40" y="200" width="120" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="3" value="ingestion.py&#10;(Python Extractor)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="220" y="210" width="120" height="60" as="geometry" />
        </mxCell>

        <mxCell id="4" value="Google BigQuery&#10;(Data Warehouse)&#10;raw_* tables" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="400" y="200" width="120" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="5" value="elt_pipeline.py&#10;(ELT &amp; DQ Tests)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="580" y="210" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="6" value="Star Schema&#10;(dim_stations, fact_trips)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="760" y="200" width="120" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="7" value="analysis.py&#10;(Pandas EDA)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="760" y="340" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="8" value="orchestrator.py&#10;(Pipeline Trigger &amp; Scheduler)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="350" y="60" width="230" height="40" as="geometry" />
        </mxCell>

        <mxCell id="9" value="Business Report PDF&#10;(Recommendations)" style="shape=document;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="760" y="460" width="120" height="80" as="geometry" />
        </mxCell>

        <!-- Edges -->
        <mxCell id="e1" edge="1" source="2" target="3" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" edge="1" source="3" target="4" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" edge="1" source="4" target="5" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" edge="1" source="5" target="6" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e5" edge="1" source="6" target="7" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e6" edge="1" source="7" target="9" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e7" edge="1" source="8" target="3" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e8" edge="1" source="8" target="5" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e9" edge="1" source="8" target="7" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

with open("pipeline_architecture.drawio", "w") as f:
    f.write(xml_content)

print("Architecture Diagram pipeline_architecture.drawio generated.")
