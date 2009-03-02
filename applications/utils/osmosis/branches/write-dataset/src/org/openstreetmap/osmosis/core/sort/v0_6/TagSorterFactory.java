// License: GPL. Copyright 2007-2008 by Brett Henderson and other contributors.
package org.openstreetmap.osmosis.core.sort.v0_6;

import org.openstreetmap.osmosis.core.pipeline.common.TaskConfiguration;
import org.openstreetmap.osmosis.core.pipeline.common.TaskManager;
import org.openstreetmap.osmosis.core.pipeline.common.TaskManagerFactory;
import org.openstreetmap.osmosis.core.pipeline.v0_6.SinkSourceManager;


/**
 * The task manager factory for a tag sorter.
 * 
 * @author Brett Henderson
 */
public class TagSorterFactory extends TaskManagerFactory {
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	protected TaskManager createTaskManagerImpl(TaskConfiguration taskConfig) {
		
		return new SinkSourceManager(
			taskConfig.getId(),
			new TagSorter(),
			taskConfig.getPipeArgs()
		);
	}
}
