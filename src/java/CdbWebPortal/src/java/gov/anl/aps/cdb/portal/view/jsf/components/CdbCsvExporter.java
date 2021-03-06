/*
 * Copyright (c) UChicago Argonne, LLC. All rights reserved.
 * See LICENSE file.
 */
package gov.anl.aps.cdb.portal.view.jsf.components;

import gov.anl.aps.cdb.portal.view.jsf.utilities.UiComponentUtility;
import java.util.HashMap;
import javax.faces.component.UIComponent;
import javax.faces.component.html.HtmlGraphicImage;
import javax.faces.component.html.HtmlOutputLink;
import javax.faces.context.FacesContext;
import org.primefaces.component.celleditor.CellEditor;
import org.primefaces.component.export.CSVExporter;

/**
 * CDB CSV exporter class.
 *
 * Overrides standard CSV exporter in order to use display values for HTTP links.
 *
 * @see
 * http://stackoverflow.com/questions/14411389/pdataexporter-does-not-recognize-pcelleditor/14413932#14413932
 */
public class CdbCsvExporter extends CSVExporter {

    private final HashMap<UIComponent, String> exportValueMap = new HashMap<>();

    @Override
    protected String exportValue(FacesContext context, UIComponent component) {
        // If parent component already has export value set, return empty string.
        if (exportValueMap.containsKey(component.getParent())) {
            return "";
        }

        // If parent component has export value attribute, use that for export values
        String exportValue = UiComponentUtility.getParentComponentExportValue(component);
        if (exportValue != null) {
            exportValueMap.put(component.getParent(), exportValue);
            return exportValue;
        }

        // Clear export value map in order to get next datatable row.
        exportValueMap.clear();

        // Find export values for various component types, defaulting to base class result.
        if (component instanceof CellEditor) {
            // Get editor output facet
            return exportValue(context, ((CellEditor) component).getFacet("output"));
        } else if (component instanceof HtmlGraphicImage) {
            // Get image alt attribute
            return (String) component.getAttributes().get("alt");
        } else if (component instanceof HtmlOutputLink) {
            // Go over all link children and combine their exported values
            HtmlOutputLink link = (HtmlOutputLink) component;
            String value = "";
            if (link.getChildCount() > 0) {
                String delimiter = "";
                for (UIComponent childComponent : link.getChildren()) {
                    String childValue = (String) super.exportValue(context, childComponent);
                    value += delimiter + childValue;
                }
            } else {
                value = (String) super.exportValue(context, component);
            }
            return value;
        } else {
            return super.exportValue(context, component);
        }
    }

}
