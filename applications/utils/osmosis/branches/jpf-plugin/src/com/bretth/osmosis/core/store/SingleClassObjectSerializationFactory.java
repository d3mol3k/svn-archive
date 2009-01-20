// License: GPL. Copyright 2007-2008 by Brett Henderson and other contributors.
package com.bretth.osmosis.core.store;


/**
 * An object reader and writer factory providing object serialisation
 * capabilities where only a single class type will be stored.
 * 
 * @author Brett Henderson
 */
public class SingleClassObjectSerializationFactory implements ObjectSerializationFactory {
	
	private Class<?> storeableType;
	
	
	/**
	 * Creates a new instance.
	 * 
	 * @param storeableType
	 *            The class type to be supported.
	 */
	public SingleClassObjectSerializationFactory(Class<?> storeableType) {
		this.storeableType = storeableType;
	}
	
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public ObjectReader createObjectReader(StoreReader storeReader, StoreClassRegister storeClassRegister) {
		return new SingleClassObjectReader(storeReader, storeClassRegister, storeableType);
	}
	
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public ObjectWriter createObjectWriter(StoreWriter storeWriter, StoreClassRegister storeClassRegister) {
		return new SingleClassObjectWriter(storeWriter, storeClassRegister, storeableType);
	}
}
