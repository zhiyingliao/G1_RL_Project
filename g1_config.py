from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class G1RoughCfg( LeggedRobotCfg ):
    class env( LeggedRobotCfg.env ):
        num_envs = 4096
        num_actions = 27           
        num_observations = 93     
        num_privileged_obs = None

    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.74] 
        default_joint_angles = {
            'left_hip_pitch_joint': -0.15, 
            'left_knee_joint': 0.4,
            'left_ankle_pitch_joint': -0.25,
            'right_hip_pitch_joint': -0.15,
            'right_knee_joint': 0.4,
            'right_ankle_pitch_joint': -0.25,
            'left_hip_roll_joint': 0.0,
            'right_hip_roll_joint': 0.0,
            'left_hip_yaw_joint': 0.0,
            'right_hip_yaw_joint': 0.0,
            'left_ankle_roll_joint': 0.0,
            'right_ankle_roll_joint': 0.0,
            'waist_yaw_joint': 0.0,
            'waist_roll_joint': 0.0, 
            'waist_pitch_joint': 0.0,
            'left_shoulder_pitch_joint': 0.2,
            'left_shoulder_roll_joint': 0.1,
            'left_shoulder_yaw_joint': 0.0,
            'left_elbow_joint': 0.3,
            'right_shoulder_pitch_joint': 0.2,
            'right_shoulder_roll_joint': -0.1,
            'right_shoulder_yaw_joint': 0.0,
            'right_elbow_joint': 0.3,
            'left_wrist_roll_joint': 0.0,
            'left_wrist_pitch_joint': 0.0,
            'left_wrist_yaw_joint': 0.0,
            'right_wrist_roll_joint': 0.0,
            'right_wrist_pitch_joint': 0.0,
            'right_wrist_yaw_joint': 0.0,
            'left_hand_finger_joint': 0.0, 
            'right_hand_finger_joint': 0.0,
        }

    # 注意这里的缩进！必须与 init_state 平级
    class rewards( LeggedRobotCfg.rewards ):
        class scales( LeggedRobotCfg.rewards.scales ):
            # 标准基线权重，足够让人形跑起来
            tracking_lin_vel = 10.0      
            tracking_ang_vel = 0.5      
            lin_vel_z = -4.0            
            ang_vel_xy = -0.1          
            orientation = -5.0          
            dof_vel = -0.001           # 抑制关节过快转动
            dof_acc = -1e-6          
            base_height = -50.0
            feet_air_time = 1.0        # 鼓励迈步
            collision = -1.0           
            action_rate = -2.0        
            stalling = -0.0            # 前期先不要加重静止惩罚，避免崩溃
            torques = -0.0001
            dof_pos_limits = -10.0

    class domain_rand( LeggedRobotCfg.domain_rand ):
        randomize_friction = True
        friction_range = [0.5, 1.25]
        randomize_base_mass = True
        added_mass_range = [-1.0, 1.0]
        push_robots = True            # 恢复正常推力，这是必需的
        push_interval_s = 5           
        max_push_vel_xy = 1.0         

    class control( LeggedRobotCfg.control ):
        stiffness = {
            'joint': 200.0, 
            'hip': 200.0, 
            'knee': 150.0, 
            'ankle': 80.0, 
            'waist': 200.0, 
            'shoulder': 40.0, 
            'elbow': 40.0
        } 
        damping = {
            'joint': 5.0, 
            'hip': 8.0, 
            'knee': 10.0, 
            'ankle': 4.0, 
            'waist': 5.0, 
            'shoulder': 2.0, 
            'elbow': 2.0
        }     
        action_scale = 0.25          
        decimation = 4            

    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/g1/g1.urdf'
        name = "g1"
        foot_name = "ankle" 
        terminate_after_contacts_on = ["pelvis", "head", "waist", "shoulder", "elbow"]
        self_collisions = 0


class G1RoughCfgPPO( LeggedRobotCfgPPO ):
    class policy( LeggedRobotCfgPPO.policy ):
        init_noise_std = 1.0      # 恢复正常初始噪声
        
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.001       # [核心修改] 降级探索率，防止打颤
        learning_rate = 1.e-3     # [核心修改] 恢复正常学习率
        max_grad_norm = 1.0

    class runner( LeggedRobotCfgPPO.runner ):
        max_iterations = 1000 
        run_name = 'g1_baseline'
        experiment_name = 'g1_walking'