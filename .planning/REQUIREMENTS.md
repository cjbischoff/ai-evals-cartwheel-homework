# Requirements

## v1 Requirements

### MOD1 — Support Agent & Tracing

- [ ] **MOD1-HW1-01**: `get_policy(ctx, policy_id)` returns matching policy doc or error
- [ ] **MOD1-HW1-02**: `search_products(ctx, query, store_id, max_price_usd, limit)` returns filtered products
- [ ] **MOD1-HW1-03**: `list_my_orders(ctx)` returns current user's orders
- [ ] **MOD1-HW1-04**: `cancel_order(ctx, order_id)` cancels an eligible order with refund
- [ ] **MOD1-HW1-05**: `find_order(ctx, query)` searches user's orders by text
- [ ] **MOD1-HW2-01**: Authenticated session creation endpoint
- [ ] **MOD1-HW2-02**: Authenticated message posting endpoint
- [ ] **MOD1-HW2-03**: Tracing attributes on tool result spans
- [ ] **MOD1-HW2-04**: Permission-denied attributes on trace spans
- [ ] **MOD1-HW2-05**: Auth tests verifying endpoint security
- [ ] **MOD1-HW3-01**: Support scenario dataset with varied scenarios
- [ ] **MOD1-HW3-02**: Trace export from Langfuse
- [ ] **MOD1-HW3-03**: Validate scenario schema and final dataset

### MOD2 — Trace Review & LLM Judges

- [ ] **MOD2-HW4-01**: Review exported traces and define failure modes
- [ ] **MOD2-HW4-02**: Document failure mode definitions with examples
- [ ] **MOD2-HW5-01**: Develop and test one LLM judge
- [ ] **MOD2-HW5-02**: Validate judge against human-labeled data

### MOD3 — CI & Monitoring

- [ ] **MOD3-HW6-01**: Build CI pipeline for Cartwheel agent
- [ ] **MOD3-HW6-02**: Automated evaluation in CI
- [ ] **MOD3-HW7-01**: Monitor one failure mode post-deployment
- [ ] **MOD3-HW7-02**: Configure monitoring alerts

### MOD5 — Optimization

- [ ] **MOD5-HW8-01**: Improve accuracy on one failure mode
- [ ] **MOD5-HW8-02**: Pareto frontier comparison of agent configurations
- [ ] **MOD5-HW9-01**: Reduce token usage
- [ ] **MOD5-HW9-02**: Implement prompt caching
- [ ] **MOD5-HW9-03**: Build model cascade
- [ ] **MOD5-HW9-04**: Compare configurations by score and cost

## v2 (Deferred)

None — all course requirements are in scope.

## Out of Scope

- Modifying course-provided test oracles or evaluation fixtures
- Weakening auth/permission system
- Features outside the course assignments
- Production deployment or real infrastructure

## Traceability

| Phase | Module | Requirements |
|-------|--------|-------------|
| 1 | Module 1 | MOD1-HW1-01 through MOD1-HW3-03 |
| 2 | Module 2 | MOD2-HW4-01 through MOD2-HW5-02 |
| 3 | Module 3 | MOD3-HW6-01 through MOD3-HW7-02 |
| 4 | Module 5 | MOD5-HW8-01 through MOD5-HW9-04 |
