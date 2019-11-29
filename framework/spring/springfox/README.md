### 文档生成流程

DocumentationPluginsBootstrapper

该类实现了SmartLifecycle接口，在ioc容器启动过程中执行refresh()->finishRefresh()->getLifecycleProcessor().onRefresh()

```
 private void scanDocumentation(DocumentationContext context) {
    try {
      scanned.addDocumentation(resourceListing.scan(context));
    } catch (Exception e) {
      log.error(String.format("Unable to scan documentation context %s", context.getGroupName()), e);
    }
  }
```

ApiDocumentationScanner

```
public Documentation scan(DocumentationContext context) {
    ApiListingReferenceScanResult result = apiListingReferenceScanner.scan(context);
    ApiListingScanningContext listingContext = new ApiListingScanningContext(context,
        result.getResourceGroupRequestMappings());

    Multimap<String, ApiListing> apiListings = apiListingScanner.scan(listingContext);
    Set<Tag> tags = toTags(apiListings);
    tags.addAll(context.getTags());
    DocumentationBuilder group = new DocumentationBuilder()
        .name(context.getGroupName())
        .apiListingsByResourceGroupName(apiListings)
        .produces(context.getProduces())
        .consumes(context.getConsumes())
        .host(context.getHost())
        .schemes(context.getProtocols())
        .basePath(context.getPathProvider().getApplicationBasePath())
        .extensions(context.getVendorExtentions())
        .tags(tags);

    Set<ApiListingReference> apiReferenceSet = newTreeSet(listingReferencePathComparator());
    apiReferenceSet.addAll(apiListingReferences(apiListings, context));

    ResourceListing resourceListing = new ResourceListingBuilder()
        .apiVersion(context.getApiInfo().getVersion())
        .apis(from(apiReferenceSet).toSortedList(context.getListingReferenceOrdering()))
        .securitySchemes(context.getSecuritySchemes())
        .info(context.getApiInfo())
        .build();
    group.resourceListing(resourceListing);
    return group.build();
  }
```

DocumentationPluginsManager

```
DocumentationPluginsManager
```

