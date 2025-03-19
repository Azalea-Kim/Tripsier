## 设计思路
- Destination，Accommodation and Attractions
- 选择顺序：旅行天数  ->  Destination  ->  Attraction  ->  Accommodation
- 自动计算总价格
- 用户可以随时修改 Plan 内容
## 功能
1. 系统向用户提供：
   - Destination：源于用户搜索
   - Attraction：附属于Destination
   - Accommodation：附属于Destination
2. 用户计划流程：
   1. 用户选择旅行的总时间，系统将提供给游客Destination选项，每日只能选择一个Destination
   2. 选择完Destination后，可以选择Attraction，**暂时无限制**
   4. 最后选择Accommodation，展示当前Destination所有可选项，选择无限制（考虑是否需要根据某种规则推荐）
3. 若多天计划，则遵循如下规则：
   1.  Destination等的选择全部不做限制，但游玩路线等可以根据某种规则推荐
   2. 采用类似于翻页表单的前端，允许跨日计划：
        - 即第一天计划完后可以直接计划第三天，再返回计划第二天或修改第一天计划
        - 不做草稿本，即若计划未确认就退出计划界面，不保留先前的计划记录
   
## 附加功能
