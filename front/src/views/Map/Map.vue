<template>
  <div :id="elementId" :style="{ width, height }">
    <!-- daum kakao map -->
  </div>
</template>

<script>
import Map from '@/views/Map/index'

export default {
  props: {
    elementId: { //Map을 생성할 곳의 Element id
      type: String,
      required: true,
    },
    markers: {
      type: Array,
      default () {
        return []
      },
      required: false,
    },
    width: {
      type: String,
      required: false,
      default: '100%',
    },
    height: {
      type: String,
      required: false,
      default: '640px',
    },
  },
  data () {
    return {
      map: null,
    }
  },
  watch: {
    markers: {
      handler () {
        if (typeof window === 'undefined') return // SSR
        this.initMap(this.markers)
      },
      immediate: true,
    },
  },
  methods: {
    async initMap (markers) {
      if (!this.map) {
        const map = new Map()
        await map.mount(this.elementId)

        // map.addMarkerClusters([
        //   {
        //     key: 'cluster1',
        //     color: '#222529',
        //     zIndex: 0,
        //     singleIconURL: ClusterIcon1,
        //   },
        //   {
        //     key: 'cluster2',
        //     color: '#209cee',
        //     zIndex: 1,
        //     singleIconURL: ClusterIcon2,
        //   },
        // ])

        this.map = map
      } else {
        this.map.clearMarkers()
      }

      this.map.addMarkers(
        markers.map(
          (marker) => {
            const { name, type, location: { lat, lng } } = marker
            return {
              lat,
              lng,
              clusterKey: type,
              title: name,
              onClick: () => {
                this.$emit('click-marker', marker)
              },
            }
          }
        )
      )
    },
    setCenter (lat, lng) {
      this.map && this.map.setCenter({ lat, lng, maxLevel: 10 })
    },
  },
}
</script>
