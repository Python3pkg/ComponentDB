/*
 * Copyright (c) UChicago Argonne, LLC. All rights reserved.
 * See LICENSE file.
 */
package gov.anl.aps.cdb.portal.model.db.beans;

import gov.anl.aps.cdb.portal.model.db.entities.ItemElementRelationship;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;

/**
 *
 * @author djarosz
 */
@Stateless
public class ItemElementRelationshipFacade extends CdbEntityFacade<ItemElementRelationship> {

    @PersistenceContext(unitName = "CdbWebPortalPU")
    private EntityManager em;

    @Override
    protected EntityManager getEntityManager() {
        return em;
    }

    public ItemElementRelationshipFacade() {
        super(ItemElementRelationship.class);
    }
    
    public ItemElementRelationship findItemElementRelationshipByNameAndItemElementId(String relationshipTypeName, int itemElementId) {
        try{
            return (ItemElementRelationship) em
                    .createNamedQuery("ItemElementRelationship.findByRelationshipTypeNameAndFirstElementId")
                    .setParameter("relationshipTypeName", relationshipTypeName)
                    .setParameter("itemElementId", itemElementId)
                    .getSingleResult();
        } catch (NoResultException ex) {
            
        }
        return null;
    }
    
}
