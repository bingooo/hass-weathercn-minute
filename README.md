# HomeAssistant 临近天气预报
中国地区临近天气预报

## 安装/更新

#### 方法1: [HACS (**点击这里安装**)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bingooo&repository=hass-weathercn-minute&category=integration)

#### 方法2: 手动安装
> [下载](https://github.com/bingooo/hass-weathercn-minute/archive/main.zip) 解压并复制 `custom_components/hass-weathercn-minute` 文件夹到HA配置目录下的`custom_components` 文件夹内


## 配置

> 配置 > 设备与服务 > 集成 > 添加集成 > 搜索 "临近天气预报"

## 可视化 
### 雷达降雨量可视化（使用  [ApexCharts Card](https://github.com/RomRider/apexcharts-card)）

<img width="500" alt="with_apexcharts" src="https://github.com/bingooo/hass-weathercn-minute/assets/1782621/3368acdd-41cd-479d-84b5-959ff9df3b39">

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: 临近降水预报
graph_span: 2h
span:
  start: minute
apex_config:
  chart:
    height: 150px
series:
  - entity: sensor.minute_summary
    data_generator: |
      const start_at = new Date(entity.attributes.start_at)
      return entity.attributes.values.map((entry, index) => {
        const time = new Date(start_at.getTime() + index * 5 * 60 * 1000);
        return [time, entry];
      });
    type: area
    show:
      in_header: false

```

### 更多可视化（使用 [ApexCharts Card](https://github.com/RomRider/apexcharts-card) + [Mushroom](https://github.com/piitaya/lovelace-mushroom) + [vertical-stack-in-card](https://github.com/ofekashery/vertical-stack-in-card)）

<img width="505" alt="with_apexcharts_and_mushroom" src="https://github.com/bingooo/hass-weathercn-minute/assets/1782621/1ce2fd8b-9b31-48d0-a5d8-841c6a566bc3">

```yaml
type: custom:vertical-stack-in-card
horizontal: true
cards:
  - type: custom:mushroom-entity-card
    entity: sensor.minute_summary
  - type: custom:apexcharts-card
    header:
      show: false
      title: 临近降水预报
    graph_span: 2h
    layout: minimal
    span:
      start: minute
    now:
      show: true
      color: red
    apex_config:
      chart:
        height: 60px
    series:
      - entity: sensor.minute_summary
        data_generator: |
          const start_at = new Date(entity.attributes.start_at)
          return entity.attributes.values.map((entry, index) => {
            const time = new Date(start_at.getTime() + index * 5 * 60 * 1000);
            return [time, entry];
          });
        type: area
        show:
          in_header: false
```

### 实体截图
<img src="https://github.com/bingooo/hass-weathercn-minute/assets/1782621/6129cf84-c274-4319-9769-d91b8bed647d" width="400">
