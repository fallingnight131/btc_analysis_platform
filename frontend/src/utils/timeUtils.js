/**
 * 时间转换工具函数
 * 将UTC时间转换为北京时间(UTC+8)
 */

/**
 * 将UTC时间字符串转换为北京时间
 * @param {string} utcTimeStr - UTC时间字符串 (如 "2025-11-10 19:41")
 * @returns {string} - 北京时间字符串
 */
export function utcToBeijing(utcTimeStr) {
  if (!utcTimeStr) return ''
  
  try {
    // 解析UTC时间
    const utcDate = new Date(utcTimeStr + ' UTC')
    
    // 转换为北京时间 (UTC+8)
    return utcDate.toLocaleString('zh-CN', {
      timeZone: 'Asia/Shanghai',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    })
  } catch (error) {
    console.error('时间转换错误:', error)
    return utcTimeStr
  }
}

/**
 * 将UTC时间字符串转换为北京时间(短格式)
 * @param {string} utcTimeStr - UTC时间字符串
 * @returns {string} - 北京时间字符串 (MM-DD HH:mm)
 */
export function utcToBeijingShort(utcTimeStr) {
  if (!utcTimeStr) return ''
  
  try {
    const utcDate = new Date(utcTimeStr + ' UTC')
    
    return utcDate.toLocaleString('zh-CN', {
      timeZone: 'Asia/Shanghai',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    })
  } catch (error) {
    console.error('时间转换错误:', error)
    return utcTimeStr
  }
}

/**
 * 批量转换时间数组
 * @param {Array<string>} timestamps - UTC时间字符串数组
 * @returns {Array<string>} - 北京时间字符串数组
 */
export function convertTimestamps(timestamps) {
  if (!Array.isArray(timestamps)) return []
  return timestamps.map(ts => utcToBeijing(ts))
}

/**
 * 批量转换时间数组(短格式)
 * @param {Array<string>} timestamps - UTC时间字符串数组
 * @returns {Array<string>} - 北京时间字符串数组 (短格式)
 */
export function convertTimestampsShort(timestamps) {
  if (!Array.isArray(timestamps)) return []
  return timestamps.map(ts => utcToBeijingShort(ts))
}

/**
 * 获取当前北京时间
 * @returns {string} - 当前北京时间字符串
 */
export function getCurrentBeijingTime() {
  return new Date().toLocaleString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}
