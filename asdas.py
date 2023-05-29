import pclpy.pcl as pcl

# Create a StatisticalOutlierRemoval filter object
outlier_filter = pcl.StatisticalOutlierRemoval.PointXYZ()

# Set the parameters for the filter
outlier_filter.setMeanK(50)  # Number of neighbors to use for mean distance estimation
outlier_filter.setStddevMulThresh(1.0)  # Standard deviation threshold

# Load your fused point cloud from previous steps (combined_cloud)
fused_cloud = pcl.PointCloud.PointXYZ()
# ... Load your point cloud data into fused_cloud

# Apply the StatisticalOutlierRemoval filter to the fused point cloud
filtered_cloud = pcl.PointCloud.PointXYZ()
outlier_filter.setInputCloud(fused_cloud)
outlier_filter.filter(filtered_cloud)

# Process the filtered point cloud as needed
process_filtered_cloud(filtered_cloud)
