"""
时间日期工具模块
提供时间日期查询功能
"""

from datetime import datetime
from typing import Dict, Any

class DateTimeTool:
    """时间日期工具类"""
    
    def __init__(self):
        self.time_formats = {
            'full': '%Y-%m-%d %H:%M:%S',
            'date': '%Y-%m-%d',
            'time': '%H:%M:%S',
            'simple': '%m-%d %H:%M'
        }
    
    def get_current_time(self) -> str:
        """获取当前时间"""
        try:
            current_time = datetime.now()
            formatted_time = current_time.strftime(self.time_formats['full'])
            return f"当前时间: {formatted_time}"
        except Exception as e:
            return f"❌ 获取时间失败: {e}"
    
    def get_current_date(self) -> str:
        """获取当前日期"""
        try:
            current_date = datetime.now()
            formatted_date = current_date.strftime(self.time_formats['date'])
            return f"当前日期: {formatted_date}"
        except Exception as e:
            return f"❌ 获取日期失败: {e}"
    
    def get_time_info(self) -> str:
        """获取时间信息"""
        try:
            now = datetime.now()
            time_info = {
                'year': now.year,
                'month': now.month,
                'day': now.day,
                'hour': now.hour,
                'minute': now.minute,
                'second': now.second,
                'weekday': now.strftime('%A'),
                'timezone': '本地时间'
            }
            
            info_str = f"📅 时间信息:\n"
            info_str += f"  - 年份: {time_info['year']}\n"
            info_str += f"  - 月份: {time_info['month']}\n"
            info_str += f"  - 日期: {time_info['day']}\n"
            info_str += f"  - 时间: {time_info['hour']:02d}:{time_info['minute']:02d}:{time_info['second']:02d}\n"
            info_str += f"  - 星期: {time_info['weekday']}\n"
            info_str += f"  - 时区: {time_info['timezone']}"
            
            return info_str
        except Exception as e:
            return f"❌ 获取时间信息失败: {e}"
    
    def format_time(self, time_format: str = 'full') -> str:
        """格式化时间"""
        try:
            if time_format not in self.time_formats:
                time_format = 'full'
            
            current_time = datetime.now()
            formatted_time = current_time.strftime(self.time_formats[time_format])
            return f"格式化时间 ({time_format}): {formatted_time}"
        except Exception as e:
            return f"❌ 格式化时间失败: {e}"
    
    def get_time_difference(self, target_time: str) -> str:
        """计算时间差"""
        try:
            # 解析目标时间
            target = datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S')
            current = datetime.now()
            
            diff = target - current
            
            if diff.total_seconds() > 0:
                return f"距离 {target_time} 还有 {diff.days} 天 {diff.seconds // 3600} 小时"
            else:
                return f"{target_time} 已经过去 {abs(diff.days)} 天 {abs(diff.seconds // 3600)} 小时"
        except Exception as e:
            return f"❌ 计算时间差失败: {e}"
    
    def validate_time_format(self, time_str: str) -> bool:
        """验证时间格式"""
        try:
            datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    
    def get_supported_formats(self) -> Dict[str, str]:
        """获取支持的时间格式"""
        return {
            'full': '完整格式 (YYYY-MM-DD HH:MM:SS)',
            'date': '日期格式 (YYYY-MM-DD)',
            'time': '时间格式 (HH:MM:SS)',
            'simple': '简单格式 (MM-DD HH:MM)'
        }

# 创建全局时间工具实例
datetime_tool = DateTimeTool()

# 工具函数接口
def get_current_time() -> str:
    """获取当前时间工具函数"""
    return datetime_tool.get_current_time()

def get_current_date() -> str:
    """获取当前日期工具函数"""
    return datetime_tool.get_current_date()

def get_time_info() -> str:
    """获取时间信息工具函数"""
    return datetime_tool.get_time_info() 